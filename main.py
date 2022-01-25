import csv
import sys
from mvn import get_dependencies_group_by_project


# TODO Refactor
def write_csv(dependencies):
    with open('dependencies.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for group_id, artifactIds in dependencies.items():
            writer.writerow([group_id])
            for artifact_id, versions in artifactIds.items():
                for version, projects in versions.items():
                    writer.writerow([artifact_id, version, ",".join(projects)])


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Missing maven project path")
        sys.exit(1)

    by_project = get_dependencies_group_by_project(project_dir=sys.argv[1])

    group_ids = {}
    for project, libraries in by_project.items():
        if libraries[0] == 'none':
            continue
        for library in libraries:
            library_info = library.split(':')
            group_id = library_info[0]
            if group_id not in group_ids:
                group_ids[group_id] = {}

            artifact_id = library_info[1]
            version = library_info[3]
            scope = library_info[4]
            if artifact_id not in group_ids[group_id]:
                group_ids[group_id][artifact_id] = {}
            if version not in group_ids[group_id][artifact_id]:
                group_ids[group_id][artifact_id][version] = []
            group_ids[group_id][artifact_id][version].append(project)
    write_csv(group_ids)
