"""
Configuration Extractors - MVP Focus
Extract and measure documentation coverage for environment variables,
connection strings, and configuration parameters.
"""

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple


@dataclass
class ConfigArtifact:
    """Represents a configuration item that needs documentation"""

    name: str
    type: str  # 'env_var', 'connection_string', 'api_key', 'config_param', 'feature_flag'
    file_path: str
    line_number: int
    usage_context: Optional[str] = None  # How it's used in code
    default_value: Optional[str] = None
    is_documented: bool = False
    documentation: Optional[str] = None
    is_required: bool = True  # Required vs optional
    is_sensitive: bool = False  # Contains secrets/passwords
    validation: Optional[str] = None  # Validation rules if any


@dataclass
class ConfigCoverageResult:
    """Coverage result for configuration documentation"""

    total_configs: int
    documented_configs: int
    coverage_percentage: float
    configs_by_type: Dict[str, List[ConfigArtifact]] = field(default_factory=dict)
    undocumented_configs: List[ConfigArtifact] = field(default_factory=list)
    critical_undocumented: List[ConfigArtifact] = field(
        default_factory=list
    )  # Sensitive/required but undocumented

    @property
    def passed(self) -> bool:
        """Check if coverage meets minimum threshold"""
        # Higher threshold for configs since they're critical
        return self.coverage_percentage >= 90.0

    @property
    def risk_score(self) -> float:
        """Calculate risk score based on undocumented critical configs"""
        if self.total_configs == 0:
            return 0.0
        critical_count = len(self.critical_undocumented)
        return (critical_count / self.total_configs) * 100


class ConfigurationExtractor:
    """Extract configuration artifacts from codebases"""

    # Common patterns for different languages
    ENV_PATTERNS = {
        "python": [
            (r'os\.environ\.get\([\'"](\w+)[\'"]', "env_var"),
            (r'os\.environ\[[\'"](\w+)[\'"]\]', "env_var"),
            (r'os\.getenv\([\'"](\w+)[\'"]', "env_var"),
            (r'config\[[\'"](\w+)[\'"]\]', "config_param"),
            (r"settings\.(\w+)", "config_param"),
        ],
        "javascript": [
            (r"process\.env\.(\w+)", "env_var"),
            (r'process\.env\[[\'"](\w+)[\'"]\]', "env_var"),
            (r'config\.get\([\'"]([^\'\"]+)[\'\"]\)', "config_param"),
            (r"import\.meta\.env\.(\w+)", "env_var"),  # Vite
        ],
        "typescript": [
            (r"process\.env\.(\w+)", "env_var"),
            (r'process\.env\[[\'"](\w+)[\'"]\]', "env_var"),
            (r'ConfigService\.get\([\'"]([^\'"]+)[\'"]', "config_param"),  # NestJS
        ],
        "java": [
            (r'System\.getenv\("(\w+)"\)', "env_var"),
            (r'@Value\("\$\{([^}]+)\}"', "config_param"),  # Spring
            (r'properties\.getProperty\("([^"]+)"', "config_param"),
        ],
        "dotnet": [
            (r'Environment\.GetEnvironmentVariable\("(\w+)"\)', "env_var"),
            (r'Configuration\["([^"]+)"\]', "config_param"),
            (r'ConfigurationManager\.AppSettings\["([^"]+)"\]', "config_param"),
        ],
    }

    # Patterns that indicate sensitive data
    SENSITIVE_PATTERNS = [
        "PASSWORD",
        "SECRET",
        "KEY",
        "TOKEN",
        "CREDENTIAL",
        "AUTH",
        "PRIVATE",
        "CERT",
        "SALT",
        "HASH",
    ]

    # Connection string patterns
    CONNECTION_PATTERNS = [
        (r"([A-Z_]+)(?:_URL|_URI|_ENDPOINT|_CONNECTION|_CONN_STR)", "connection_string"),
        (r'(mongodb|postgres|mysql|redis|elastic|kafka|rabbitmq)://[^\'"\s]+', "connection_string"),
        (r"Data Source=.*;.*Password=.*", "connection_string"),  # SQL Server
    ]

    def extract_configs(self, project_path: str) -> List[ConfigArtifact]:
        """Extract all configuration artifacts from a project"""
        path = Path(project_path)
        configs = []

        # Scan source files
        for ext, patterns in self.get_patterns_for_project(path).items():
            for file_path in path.rglob(f"*{ext}"):
                # Skip test and vendor directories
                if self.should_skip_file(file_path):
                    continue

                file_configs = self.extract_from_file(file_path, patterns)
                configs.extend(file_configs)

        # Scan .env files
        env_configs = self.extract_from_env_files(path)
        configs.extend(env_configs)

        # Scan configuration files
        config_file_configs = self.extract_from_config_files(path)
        configs.extend(config_file_configs)

        # Check documentation
        self.check_documentation(configs, path)

        # Deduplicate by name
        unique_configs = {}
        for config in configs:
            if config.name not in unique_configs:
                unique_configs[config.name] = config
            else:
                # Merge information
                existing = unique_configs[config.name]
                if not existing.is_documented and config.is_documented:
                    existing.is_documented = True
                    existing.documentation = config.documentation

        return list(unique_configs.values())

    def get_patterns_for_project(self, path: Path) -> Dict[str, List[Tuple]]:
        """Determine which patterns to use based on project type"""
        patterns = {}

        # Python
        if any(path.rglob("*.py")):
            patterns[".py"] = self.ENV_PATTERNS["python"]

        # JavaScript/TypeScript
        if (path / "package.json").exists():
            patterns[".js"] = self.ENV_PATTERNS["javascript"]
            patterns[".jsx"] = self.ENV_PATTERNS["javascript"]
            patterns[".ts"] = self.ENV_PATTERNS.get("typescript", self.ENV_PATTERNS["javascript"])
            patterns[".tsx"] = self.ENV_PATTERNS.get("typescript", self.ENV_PATTERNS["javascript"])

        # Java
        if any(path.rglob("*.java")):
            patterns[".java"] = self.ENV_PATTERNS["java"]

        # .NET
        if any(path.rglob("*.cs")):
            patterns[".cs"] = self.ENV_PATTERNS["dotnet"]

        return patterns

    def should_skip_file(self, file_path: Path) -> bool:
        """Check if file should be skipped"""
        skip_dirs = [
            "node_modules",
            "venv",
            ".venv",
            "__pycache__",
            "dist",
            "build",
            "target",
            "vendor",
            ".git",
        ]

        for skip in skip_dirs:
            if skip in str(file_path):
                return True

        # Skip test files for MVP (they often have different config patterns)
        if "test" in file_path.name.lower():
            return True

        return False

    def extract_from_file(self, file_path: Path, patterns: List[Tuple]) -> List[ConfigArtifact]:
        """Extract configs from a single source file"""
        configs = []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                lines = content.split("\n")

            for pattern, config_type in patterns:
                for match in re.finditer(pattern, content):
                    config_name = match.group(1)
                    line_number = content[: match.start()].count("\n") + 1

                    # Get usage context (the line of code)
                    if line_number <= len(lines):
                        usage_context = lines[line_number - 1].strip()
                    else:
                        usage_context = None

                    # Check if sensitive
                    is_sensitive = any(
                        pattern in config_name.upper() for pattern in self.SENSITIVE_PATTERNS
                    )

                    configs.append(
                        ConfigArtifact(
                            name=config_name,
                            type=config_type,
                            file_path=str(file_path),
                            line_number=line_number,
                            usage_context=usage_context,
                            is_sensitive=is_sensitive,
                            is_documented=False,  # Will check docs later
                        )
                    )

            # Check for connection strings
            for pattern, config_type in self.CONNECTION_PATTERNS:
                for match in re.finditer(pattern, content):
                    config_name = match.group(1) if match.groups() else match.group(0)[:30]
                    line_number = content[: match.start()].count("\n") + 1

                    configs.append(
                        ConfigArtifact(
                            name=config_name,
                            type=config_type,
                            file_path=str(file_path),
                            line_number=line_number,
                            is_sensitive=True,  # Connection strings are always sensitive
                            is_documented=False,
                        )
                    )

        except Exception as e:
            print(f"Error processing {file_path}: {e}")

        return configs

    def extract_from_env_files(self, project_path: Path) -> List[ConfigArtifact]:
        """Extract configs from .env files"""
        configs = []

        # Common env file names
        env_files = [
            ".env",
            ".env.example",
            ".env.sample",
            ".env.template",
            ".env.local",
            ".env.development",
            ".env.production",
        ]

        for env_file_name in env_files:
            env_file = project_path / env_file_name
            if env_file.exists():
                try:
                    with open(env_file, "r") as f:
                        for line_no, line in enumerate(f, 1):
                            line = line.strip()

                            # Skip comments and empty lines
                            if not line or line.startswith("#"):
                                continue

                            # Parse KEY=VALUE format
                            if "=" in line:
                                key = line.split("=")[0].strip()
                                value = line.split("=", 1)[1].strip()

                                # Check if it's documented (has comment above)
                                is_documented = False
                                if line_no > 1:
                                    # Check if previous line was a comment
                                    env_file.seek(0)
                                    lines = env_file.readlines()
                                    if line_no > 1 and lines[line_no - 2].strip().startswith("#"):
                                        is_documented = True

                                is_sensitive = any(
                                    pattern in key.upper() for pattern in self.SENSITIVE_PATTERNS
                                )

                                configs.append(
                                    ConfigArtifact(
                                        name=key,
                                        type="env_var",
                                        file_path=str(env_file),
                                        line_number=line_no,
                                        default_value=value if not is_sensitive else "[REDACTED]",
                                        is_documented=is_documented,
                                        is_sensitive=is_sensitive,
                                    )
                                )

                except Exception as e:
                    print(f"Error reading {env_file}: {e}")

        return configs

    def extract_from_config_files(self, project_path: Path) -> List[ConfigArtifact]:
        """Extract from common config files (appsettings.json, config.yml, etc.)"""
        configs = []

        # JSON config files
        for json_file in project_path.rglob("*config*.json"):
            if self.should_skip_file(json_file):
                continue

            try:
                with open(json_file, "r") as f:
                    data = json.load(f)
                    flat_configs = self.flatten_json_config(data)

                    for key, value in flat_configs.items():
                        is_sensitive = any(
                            pattern in key.upper() for pattern in self.SENSITIVE_PATTERNS
                        )

                        configs.append(
                            ConfigArtifact(
                                name=key,
                                type="config_param",
                                file_path=str(json_file),
                                line_number=1,  # Can't easily determine line in JSON
                                default_value=str(value) if not is_sensitive else "[REDACTED]",
                                is_sensitive=is_sensitive,
                                is_documented=False,
                            )
                        )

            except Exception:
                pass  # Skip invalid JSON

        return configs

    def flatten_json_config(self, data: Dict, prefix: str = "") -> Dict:
        """Flatten nested JSON config to dot notation"""
        result = {}

        for key, value in data.items():
            full_key = f"{prefix}.{key}" if prefix else key

            if isinstance(value, dict):
                result.update(self.flatten_json_config(value, full_key))
            else:
                result[full_key] = value

        return result

    def check_documentation(self, configs: List[ConfigArtifact], project_path: Path):
        """Check if configs are documented in README or docs"""
        doc_files = []

        # Find documentation files
        for pattern in ["README*", "readme*", "*.md", "docs/*", "documentation/*"]:
            doc_files.extend(project_path.glob(pattern))
            doc_files.extend(project_path.rglob(pattern))

        # Read all documentation
        doc_content = []
        for doc_file in doc_files:
            if doc_file.is_file():
                try:
                    with open(doc_file, "r", encoding="utf-8") as f:
                        doc_content.append(f.read())
                except (IOError, UnicodeDecodeError):
                    pass

        all_docs = "\n".join(doc_content).upper()

        # Check each config
        for config in configs:
            # Simple check: is the config name mentioned in docs?
            if config.name.upper() in all_docs:
                config.is_documented = True

                # Try to extract documentation context
                for doc in doc_content:
                    if config.name in doc:
                        # Find the line mentioning this config
                        lines = doc.split("\n")
                        for i, line in enumerate(lines):
                            if config.name in line:
                                # Get surrounding context
                                start = max(0, i - 1)
                                end = min(len(lines), i + 2)
                                config.documentation = "\n".join(lines[start:end])
                                break
                        if config.documentation:
                            break


class ConfigCoverageCalculator:
    """Calculate configuration documentation coverage"""

    def __init__(self):
        self.extractor = ConfigurationExtractor()

    def calculate_coverage(self, project_path: str) -> ConfigCoverageResult:
        """Calculate configuration documentation coverage for a project"""
        configs = self.extractor.extract_configs(project_path)

        # Calculate metrics
        total = len(configs)
        documented = sum(1 for c in configs if c.is_documented)
        coverage = (documented / total * 100) if total > 0 else 100.0

        # Group by type
        configs_by_type = {}
        for config in configs:
            if config.type not in configs_by_type:
                configs_by_type[config.type] = []
            configs_by_type[config.type].append(config)

        # Find undocumented and critical configs
        undocumented = [c for c in configs if not c.is_documented]
        critical_undocumented = [
            c for c in undocumented if c.is_sensitive or c.type == "connection_string"
        ]

        return ConfigCoverageResult(
            total_configs=total,
            documented_configs=documented,
            coverage_percentage=coverage,
            configs_by_type=configs_by_type,
            undocumented_configs=undocumented,
            critical_undocumented=critical_undocumented,
        )

    def generate_report(self, result: ConfigCoverageResult) -> str:
        """Generate a human-readable coverage report"""
        report = []
        report.append("🔧 Configuration Documentation Coverage Report")
        report.append("=" * 60)
        report.append(f"Overall Coverage: {result.coverage_percentage:.1f}%")
        report.append(f"Total Configurations: {result.total_configs}")
        report.append(f"Documented: {result.documented_configs}")
        report.append(f"Status: {'✅ PASSED' if result.passed else '❌ FAILED (90% required)'}")

        if result.critical_undocumented:
            report.append(f"\n⚠️  RISK SCORE: {result.risk_score:.1f}%")
            report.append(f"Critical undocumented configs: {len(result.critical_undocumented)}")

        report.append("\nCoverage by Type:")
        report.append("-" * 40)
        for config_type, configs in result.configs_by_type.items():
            documented = sum(1 for c in configs if c.is_documented)
            total = len(configs)
            percentage = (documented / total * 100) if total > 0 else 0
            emoji = "✅" if percentage >= 90 else "⚠️" if percentage >= 70 else "❌"
            report.append(f"  {emoji} {config_type}: {documented}/{total} ({percentage:.1f}%)")

        # Critical undocumented configs
        if result.critical_undocumented:
            report.append("\n🚨 Critical Undocumented Configurations:")
            report.append("-" * 40)
            for config in result.critical_undocumented[:10]:  # Show top 10
                location = f"{Path(config.file_path).name}:{config.line_number}"
                report.append(f"  ❌ {config.name} ({config.type}) - {location}")
                if config.usage_context:
                    report.append(f"     Usage: {config.usage_context[:60]}...")

        # Regular undocumented configs
        if result.undocumented_configs:
            non_critical = [
                c for c in result.undocumented_configs if c not in result.critical_undocumented
            ]
            if non_critical:
                report.append("\n📝 Other Undocumented Configurations (first 10):")
                report.append("-" * 40)
                for config in non_critical[:10]:
                    report.append(f"  • {config.name} ({config.type})")

        # Recommendations
        report.append("\n💡 Recommendations:")
        report.append("-" * 40)
        if result.coverage_percentage < 90:
            report.append("  1. Document all environment variables in README.md")
            report.append("  2. Create .env.example with all required variables")
            report.append("  3. Add configuration section to documentation")

        if result.critical_undocumented:
            report.append("  ⚠️  URGENT: Document all sensitive configurations immediately!")
            report.append("     These can cause security incidents if misconfigured")

        return "\n".join(report)
