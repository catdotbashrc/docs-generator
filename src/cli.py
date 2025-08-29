#!/usr/bin/env python3
"""
DDD Command Line Interface
The main entry point for Documentation Driven Development
"""

import click
import json
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from ddd import DocumentationCoverage, DependencyExtractor, DAYLIGHTSpec
from ddd.artifact_extractors import ArtifactCoverageCalculator
from ddd.config_extractors import ConfigCoverageCalculator

console = Console()


@click.group()
def cli():
    """Documentation Driven Development - TDD for documentation coverage"""
    pass


@cli.command()
@click.argument('project_path', type=click.Path(exists=True))
@click.option('--output', '-o', help='Output file for results (JSON)')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def measure(project_path, output, verbose):
    """Measure documentation coverage for a project"""
    
    console.print(f"[bold blue]📊 Measuring documentation coverage for {project_path}[/bold blue]\n")
    
    # Extract documentation (currently just dependencies for MVP)
    extractor = DependencyExtractor()
    extracted = {
        'dependencies': extractor.extract(project_path)
    }
    
    # Measure coverage
    coverage = DocumentationCoverage()
    result = coverage.measure(extracted)
    
    # Display results
    if result.passed:
        console.print(Panel(
            f"[bold green]✅ Documentation Coverage PASSED[/bold green]\n"
            f"Overall Coverage: {result.overall_coverage:.1%}",
            title="Result"
        ))
    else:
        console.print(Panel(
            f"[bold red]❌ Documentation Coverage FAILED[/bold red]\n"
            f"Overall Coverage: {result.overall_coverage:.1%}",
            title="Result"
        ))
    
    # Show dimension breakdown
    table = Table(title="Coverage by Dimension")
    table.add_column("Dimension", style="cyan")
    table.add_column("Coverage", justify="right")
    table.add_column("Status", justify="center")
    
    for dim, score in result.dimension_scores.items():
        status = "✅" if score >= 0.85 else "⚠️" if score >= 0.70 else "❌"
        table.add_row(dim.capitalize(), f"{score:.1%}", status)
    
    console.print(table)
    
    # Show missing elements
    if result.missing_elements:
        console.print("\n[bold yellow]Missing Documentation:[/bold yellow]")
        for dim, missing in result.missing_elements.items():
            console.print(f"  • {dim}: {', '.join(missing)}")
    
    # Show recommendations
    if result.recommendations:
        console.print("\n[bold cyan]Recommendations:[/bold cyan]")
        for rec in result.recommendations[:5]:  # Show top 5
            console.print(f"  → {rec}")
    
    # Save to file if requested
    if output:
        output_data = {
            'overall_coverage': result.overall_coverage,
            'passed': result.passed,
            'dimension_scores': result.dimension_scores,
            'missing_elements': result.missing_elements,
            'recommendations': result.recommendations,
            'extracted_data': extracted
        }
        
        with open(output, 'w') as f:
            json.dump(output_data, f, indent=2, default=str)
        console.print(f"\n[green]Results saved to {output}[/green]")
    
    # Exit with error code if failed
    if not result.passed:
        exit(1)


@cli.command()
@click.argument('project_path', type=click.Path(exists=True))
@click.option('--min-coverage', '-m', default=0.85, type=float, 
              help='Minimum coverage threshold (0-1)')
def assert_coverage(project_path, min_coverage):
    """Assert that documentation meets minimum coverage (fails if not)"""
    
    console.print(f"[bold blue]🎯 Asserting documentation coverage >= {min_coverage:.0%}[/bold blue]\n")
    
    # Extract documentation
    extractor = DependencyExtractor()
    extracted = {
        'dependencies': extractor.extract(project_path)
    }
    
    # Assert coverage
    coverage = DocumentationCoverage()
    try:
        coverage.assert_coverage(extracted, minimum=min_coverage)
        console.print(f"[bold green]✅ Coverage assertion passed![/bold green]")
    except AssertionError as e:
        console.print(f"[bold red]❌ Coverage assertion failed![/bold red]")
        console.print(f"\n{e}")
        exit(1)


@cli.command()
@click.argument('project_path', type=click.Path(exists=True))
def demo(project_path):
    """Run the full DDD workflow demonstration"""
    
    console.print(Panel(
        "[bold]Documentation Driven Development Demo[/bold]\n"
        "RED → GREEN → REFACTOR",
        title="DDD Workflow"
    ))
    
    # 1. RED Phase
    console.print("\n[bold red]1. RED Phase - Define Requirements[/bold red]")
    console.print("   Documentation spec requires 90% coverage for dependencies")
    
    extractor = DependencyExtractor()
    extracted = {'dependencies': {}}  # Start with no extraction
    
    coverage = DocumentationCoverage()
    result = coverage.measure(extracted)
    console.print(f"   Initial coverage: {result.overall_coverage:.1%} ❌")
    
    # 2. GREEN Phase
    console.print("\n[bold green]2. GREEN Phase - Extract Documentation[/bold green]")
    console.print("   Running dependency extractor...")
    
    extracted = {'dependencies': extractor.extract(project_path)}
    result = coverage.measure(extracted)
    console.print(f"   Extracted coverage: {result.overall_coverage:.1%} {'✅' if result.passed else '⚠️'}")
    
    # 3. REFACTOR Phase
    console.print("\n[bold blue]3. REFACTOR Phase - Optimize Documentation[/bold blue]")
    console.print("   Would optimize for clarity and completeness")
    console.print("   Add missing fields, improve descriptions, etc.")
    
    console.print("\n[bold]Summary:[/bold]")
    console.print(f"   Final Coverage: {result.overall_coverage:.1%}")
    console.print(f"   Status: {'PASSED ✅' if result.passed else 'NEEDS IMPROVEMENT ⚠️'}")


@cli.command()
@click.argument('project_path', type=click.Path(exists=True))
@click.option('--output', '-o', help='Output file for results (JSON)')
@click.option('--min-coverage', '-m', default=85.0, type=float, 
              help='Minimum coverage threshold (0-100)')
def measure_artifacts(project_path, output, min_coverage):
    """Measure documentation coverage based on code artifacts (NEW approach)"""
    
    console.print(f"[bold blue]🎯 Artifact-Based Documentation Coverage Analysis[/bold blue]\n")
    console.print(f"[dim]Counting functions, classes, methods, and other code artifacts...[/dim]\n")
    
    # Calculate artifact-based coverage
    calculator = ArtifactCoverageCalculator()
    result = calculator.calculate_coverage(project_path)
    
    # Display results with Rich formatting
    if result.passed:
        console.print(Panel(
            f"[bold green]✅ Documentation Coverage PASSED[/bold green]\n"
            f"Coverage: {result.coverage_percentage:.1f}%\n"
            f"Documented: {result.documented_artifacts}/{result.total_artifacts} artifacts",
            title="Result"
        ))
    else:
        console.print(Panel(
            f"[bold red]❌ Documentation Coverage FAILED[/bold red]\n"
            f"Coverage: {result.coverage_percentage:.1f}% (minimum: {min_coverage}%)\n"
            f"Documented: {result.documented_artifacts}/{result.total_artifacts} artifacts",
            title="Result"
        ))
    
    # Show breakdown by type
    table = Table(title="Coverage by Artifact Type")
    table.add_column("Type", style="cyan")
    table.add_column("Documented", justify="right")
    table.add_column("Total", justify="right")
    table.add_column("Coverage", justify="right")
    table.add_column("Status", justify="center")
    
    for artifact_type, artifacts in result.artifacts_by_type.items():
        documented = sum(1 for a in artifacts if a.is_documented)
        total = len(artifacts)
        percentage = (documented / total * 100) if total > 0 else 0
        status = "✅" if percentage >= 85 else "⚠️" if percentage >= 70 else "❌"
        table.add_row(
            artifact_type.capitalize(),
            str(documented),
            str(total),
            f"{percentage:.1f}%",
            status
        )
    
    console.print(table)
    
    # Show top undocumented items
    if result.undocumented_artifacts:
        console.print("\n[bold yellow]Top Undocumented Artifacts:[/bold yellow]")
        console.print("[dim](showing first 10)[/dim]")
        for artifact in result.undocumented_artifacts[:10]:
            location = f"{Path(artifact.file_path).name}:{artifact.line_number}"
            if artifact.parent:
                name = f"{artifact.parent}.{artifact.name}"
            else:
                name = artifact.name
            console.print(f"  ❌ {artifact.type}: [cyan]{name}[/cyan] ({location})")
    
    # Save to file if requested
    if output:
        output_data = {
            'coverage_percentage': result.coverage_percentage,
            'total_artifacts': result.total_artifacts,
            'documented_artifacts': result.documented_artifacts,
            'passed': result.passed,
            'artifacts_by_type': {
                type_name: [
                    {
                        'name': a.name,
                        'file': a.file_path,
                        'line': a.line_number,
                        'documented': a.is_documented
                    }
                    for a in artifacts
                ]
                for type_name, artifacts in result.artifacts_by_type.items()
            }
        }
        
        with open(output, 'w') as f:
            json.dump(output_data, f, indent=2, default=str)
        console.print(f"\n[green]Results saved to {output}[/green]")
    
    # Exit with error code if failed
    if not result.passed:
        exit(1)


@cli.command()
@click.argument('project_path', type=click.Path(exists=True))
@click.option('--output', '-o', help='Output file for results (JSON)')
@click.option('--show-all', is_flag=True, help='Show all undocumented configs, not just critical')
def config_coverage(project_path, output, show_all):
    """🔧 Measure configuration documentation coverage (MVP DEMO)
    
    Analyzes environment variables, connection strings, and configuration
    parameters to ensure they're documented. This prevents production failures
    due to missing or misconfigured settings.
    """
    
    console.print(f"[bold blue]🔧 Configuration Documentation Coverage Analysis[/bold blue]")
    console.print(f"[dim]Scanning for environment variables, connection strings, and configs...[/dim]\n")
    
    # Calculate configuration coverage
    calculator = ConfigCoverageCalculator()
    result = calculator.calculate_coverage(project_path)
    
    # Display results with Rich formatting
    if result.passed:
        console.print(Panel(
            f"[bold green]✅ Configuration Documentation PASSED[/bold green]\n"
            f"Coverage: {result.coverage_percentage:.1f}%\n"
            f"Documented: {result.documented_configs}/{result.total_configs} configurations",
            title="Result",
            border_style="green"
        ))
    else:
        console.print(Panel(
            f"[bold red]❌ Configuration Documentation FAILED[/bold red]\n"
            f"Coverage: {result.coverage_percentage:.1f}% (minimum: 90%)\n"
            f"Documented: {result.documented_configs}/{result.total_configs} configurations\n"
            f"[bold yellow]Risk Score: {result.risk_score:.1f}%[/bold yellow]",
            title="Result",
            border_style="red"
        ))
    
    # Show breakdown by type
    table = Table(title="Coverage by Configuration Type")
    table.add_column("Type", style="cyan")
    table.add_column("Documented", justify="right")
    table.add_column("Total", justify="right")
    table.add_column("Coverage", justify="right")
    table.add_column("Status", justify="center")
    
    for config_type, configs in result.configs_by_type.items():
        documented = sum(1 for c in configs if c.is_documented)
        total = len(configs)
        percentage = (documented / total * 100) if total > 0 else 0
        status = "✅" if percentage >= 90 else "⚠️" if percentage >= 70 else "❌"
        
        # Highlight connection strings and env vars
        if config_type in ['env_var', 'connection_string']:
            table.add_row(
                f"[bold]{config_type}[/bold]",
                str(documented),
                str(total),
                f"{percentage:.1f}%",
                status
            )
        else:
            table.add_row(
                config_type,
                str(documented),
                str(total),
                f"{percentage:.1f}%",
                status
            )
    
    console.print(table)
    
    # Show critical undocumented configs (ALWAYS)
    if result.critical_undocumented:
        console.print("\n[bold red]🚨 CRITICAL: Undocumented Sensitive Configurations:[/bold red]")
        console.print("[dim]These can cause security incidents or production failures![/dim]")
        
        for config in result.critical_undocumented[:10]:
            location = f"{Path(config.file_path).name}:{config.line_number}"
            console.print(f"  ❌ [red]{config.name}[/red] ({config.type}) - {location}")
            if config.usage_context:
                console.print(f"     [dim]Usage: {config.usage_context[:60]}...[/dim]")
    
    # Show other undocumented configs
    if show_all and result.undocumented_configs:
        non_critical = [c for c in result.undocumented_configs 
                       if c not in result.critical_undocumented]
        if non_critical:
            console.print("\n[bold yellow]📝 Other Undocumented Configurations:[/bold yellow]")
            for config in non_critical[:20]:
                console.print(f"  • {config.name} ({config.type})")
    
    # Business impact message
    if not result.passed:
        console.print("\n[bold]💼 Business Impact:[/bold]")
        console.print(f"  • [red]{len(result.undocumented_configs)} configurations[/red] could cause production failures")
        console.print(f"  • [red]{len(result.critical_undocumented)} sensitive configs[/red] pose security risks")
        console.print(f"  • Estimated incident risk: [bold red]{result.risk_score:.0f}%[/bold red]")
        console.print("\n[bold]📋 Next Steps:[/bold]")
        console.print("  1. Document all environment variables in README.md")
        console.print("  2. Create .env.example with all required variables")
        console.print("  3. Add configuration reference to your documentation")
    
    # Save to file if requested
    if output:
        output_data = {
            'coverage_percentage': result.coverage_percentage,
            'total_configs': result.total_configs,
            'documented_configs': result.documented_configs,
            'passed': result.passed,
            'risk_score': result.risk_score,
            'critical_undocumented': [
                {
                    'name': c.name,
                    'type': c.type,
                    'file': c.file_path,
                    'line': c.line_number,
                    'sensitive': c.is_sensitive
                }
                for c in result.critical_undocumented
            ],
            'configs_by_type': {
                type_name: {
                    'total': len(configs),
                    'documented': sum(1 for c in configs if c.is_documented),
                    'configs': [c.name for c in configs[:10]]  # Sample
                }
                for type_name, configs in result.configs_by_type.items()
            }
        }
        
        with open(output, 'w') as f:
            json.dump(output_data, f, indent=2, default=str)
        console.print(f"\n[green]Results saved to {output}[/green]")
    
    # Exit with error code if failed
    if not result.passed:
        exit(1)


def main():
    """Main entry point"""
    cli()


if __name__ == '__main__':
    main()