#!/usr/bin/env python3
"""
Felix Learning Platform - Code Quality Checker
Analyzes code quality across the curriculum
"""

import os
import re
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class QualityIssue:
    """A code quality issue"""
    file_path: str
    line_number: int
    severity: str
    category: str
    message: str


class FelixCodeQualityChecker:
    """Checks code quality across all curriculum code"""

    def __init__(self, base_path: str = "./public/phases"):
        self.base_path = Path(base_path)
        self.issues: List[QualityIssue] = []
        self.stats = {
            "files_checked": 0,
            "lines_of_code": 0,
            "functions_found": 0,
            "classes_found": 0
        }

    def analyze_all(self) -> Dict:
        """Run full analysis on all code files"""
        print("\n🔍 Felix Code Quality Analysis")
        print("=" * 50)

        for extension in ['.py', '.ts', '.tsx']:
            self._scan_directory(self.base_path, extension)

        return self._generate_report()

    def _scan_directory(self, directory: Path, extension: str):
        """Scan directory for files with given extension"""
        for file_path in directory.rglob(f"*{extension}"):
            if 'node_modules' in str(file_path):
                continue
            self._analyze_file(file_path)

    def _analyze_file(self, file_path: Path):
        """Analyze a single file"""
        self.stats["files_checked"] += 1

        try:
            content = file_path.read_text()
            self.stats["lines_of_code"] += len(content.split('\n'))

            # Count functions and classes
            self.stats["functions_found"] += len(re.findall(r'\ndef\s+\w+', content))
            self.stats["classes_found"] += len(re.findall(r'\nclass\s+\w+', content))

            # Run quality checks
            self._check_naming_conventions(file_path, content)
            self._check_documentation(file_path, content)
            self._check_complexity(file_path, content)

        except Exception as e:
            self.issues.append(QualityIssue(
                file_path=str(file_path),
                line_number=0,
                severity="warning",
                category="read_error",
                message=f"Could not analyze: {str(e)}"
            ))

    def _check_naming_conventions(self, file_path: Path, content: str):
        """Check naming conventions"""
        # Check for snake_case variables
        snake_case_vars = re.findall(r'\b[a-z][a-z0-9_]*\s*=', content)
        camel_case_vars = re.findall(r'\b[a-z][a-z][a-z0-9]*\s*=', content)

        for match in camel_case_vars:
            if match and not any(kw in match for kw in ['class', 'def', 'import']):
                line_num = content[:content.find(match)].count('\n') + 1
                self.issues.append(QualityIssue(
                    file_path=str(file_path),
                    line_number=line_num,
                    severity="info",
                    category="naming",
                    message=f"Variable '{match}' should use snake_case"
                ))

    def _check_documentation(self, file_path: Path, content: str):
        """Check documentation coverage"""
        if file_path.suffix == '.py':
            functions = re.findall(r'\ndef\s+(\w+)', content)
            documented = len(re.findall(r':param|:type|"""', content))

            if functions and documented / len(functions) < 0.3:
                self.issues.append(QualityIssue(
                    file_path=str(file_path),
                    line_number=1,
                    severity="info",
                    category="documentation",
                    message=f"Only {documented}/{len(functions)} functions are documented"
                ))

    def _check_complexity(self, file_path: Path, content: str):
        """Check code complexity"""
        lines = content.split('\n')
        in_function = False
        function_lines = 0

        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            if stripped.startswith('def '):
                in_function = True
                function_lines = 0
            elif in_function:
                if stripped.startswith('def ') or (stripped.startswith('class ') and not stripped.startswith('class ')):
                    in_function = False
                    if function_lines > 50:
                        self.issues.append(QualityIssue(
                            file_path=str(file_path),
                            line_number=i - function_lines,
                            severity="warning",
                            category="complexity",
                            message=f"Function is {function_lines} lines - consider refactoring"
                        ))
                else:
                    function_lines += 1

    def _generate_report(self) -> Dict:
        """Generate analysis report"""
        print(f"\n📊 Statistics:")
        print(f"   Files analyzed: {self.stats['files_checked']}")
        print(f"   Lines of code: {self.stats['lines_of_code']:,}")
        print(f"   Functions found: {self.stats['functions_found']}")
        print(f"   Classes found: {self.stats['classes_found']}")

        # Group issues by category
        categories = {}
        for issue in self.issues:
            if issue.category not in categories:
                categories[issue.category] = []
            categories[issue.category].append(issue)

        print(f"\n⚠️  Issues Found: {len(self.issues)}")
        for category, issues in categories.items():
            print(f"   {category}: {len(issues)}")

        if self.issues:
            print(f"\n📝 Top Issues:")
            for issue in self.issues[:5]:
                print(f"   [{issue.severity}] {issue.file_path}:{issue.line_number}")
                print(f"      {issue.message}")

        return {
            "stats": self.stats,
            "total_issues": len(self.issues),
            "issues_by_category": {k: len(v) for k, v in categories.items()},
            "quality_score": self._calculate_score()
        }

    def _calculate_score(self) -> float:
        """Calculate overall quality score (0-100)"""
        base_score = 100
        deductions = len(self.issues) * 0.5
        return max(0, base_score - deductions)


def main():
    checker = FelixCodeQualityChecker()
    report = checker.analyze_all()

    print(f"\n🎯 Quality Score: {report['quality_score']:.1f}/100")
    print("\n✅ Analysis complete!")


if __name__ == "__main__":
    main()