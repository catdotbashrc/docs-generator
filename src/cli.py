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


def main():
    """Main entry point"""
    cli()


if __name__ == '__main__':
    main()