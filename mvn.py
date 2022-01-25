from subprocess import check_output


class MvnRunner:

    def __init__(self, project_dir):
        self.__project_dir = project_dir
        self.__exclude_transitive = 'false'

    def exclude_transitive(self):
        self.__exclude_transitive = 'true'

    def run(self):
        return check_output([
            'mvn',
            'dependency:list',
            '-f', self.__project_dir,
            '-Dsort=true',
            '-DexcludeTransitive=' + self.__exclude_transitive,
        ]).decode("utf-8")


def _get_dependencies_by_project(mvn_stdout):
    dependencies = {}
    lines = _get_lines_by_project(mvn_stdout)
    for line in lines:
        project = line[0].strip().split(' ')[0]
        for dependencyLine in line[_get_start_of_dependencies_idx(line):]:
            dependency = dependencyLine.split(' ')
            if len(dependency) == 2:
                break
            if project not in dependencies:
                dependencies[project] = []
            dependencies[project].append(dependency[4])
    return dependencies


def _get_lines_by_project(mvn_stdout):
    return list(map(lambda l: l.split('\n'), mvn_stdout.split('\x1b[1mBuilding')))[2:]  # Skip parent pom


def _get_start_of_dependencies_idx(line):
    for idx, s in enumerate(line):
        if "The following files have been resolved:" in s:
            return idx + 1
    return -1


def get_dependencies_group_by_project(project_dir='.', exclude_transitive=True):
    mvn_runner = MvnRunner(project_dir)
    if exclude_transitive:
        mvn_runner.exclude_transitive()

    return _get_dependencies_by_project(mvn_runner.run())
