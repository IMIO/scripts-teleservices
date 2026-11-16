#!/usr/bin/env python3

# This script is used to update the definition of centralized sources passerelle
# by adding the wcatoken=false parameter to the filter_expression of the queries
# of the resources actualites, evenements and annuaire.
# see WEB-4156

import json
import subprocess

OUTPUT_FILE_PATH = "/tmp/centralized_sources.json"
OUTPUT_FILE_PATH_FILTERED = "/tmp/centralized_sources_filtered.json"


def export_centralized_sources(output_file_path):
    try:
        subprocess.run(
            [
                "sudo",
                "-u",
                "passerelle",
                "passerelle-manage",
                "tenant_command",
                "export_site",
                "--slugs",
                "evenements",
                "actualites",
                "annuaire",
                "--all-tenants",
                "--output",
                output_file_path,
            ]
        )
    except Exception as e:
        raise Exception(f"Error during export: {e}")


def import_centralized_sources(output_file_path_filtered):
    try:
        subprocess.run(
            [
                "sudo",
                "-u",
                "passerelle",
                "passerelle-manage",
                "tenant_command",
                "import_site",
                "--all-tenants",
                "--overwrite",
                output_file_path_filtered,
            ]
        )
    except Exception as e:
        raise Exception(f"Error during import: {e}")


def update_json_file(file_path, output_file_path) -> int:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        filtered_resources = []
        filtered_count = 0
        for resource in data.get("resources", []):
            if resource.get("slug") in ["actualites", "evenements", "annuaire"]:
                for query in resource.get("queries", []):
                    if "filter_expression" in query:
                        if "\r\nwcatoken=false" not in query["filter_expression"]:
                            filtered_count += 1
                            query["filter_expression"] += "\r\nwcatoken=false"
                filtered_resources.append(resource)

        data["resources"] = filtered_resources

        with open(output_file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        return filtered_count
    except Exception as e:
        raise Exception(f"Error during update: {e}")


def main():
    try:
        export_centralized_sources(OUTPUT_FILE_PATH)
        print(f"Export done!, output file: {OUTPUT_FILE_PATH}")
        filtered_count = update_json_file(OUTPUT_FILE_PATH, OUTPUT_FILE_PATH_FILTERED)
        print(
            f"Update done!, {filtered_count} resources modified... output file: {OUTPUT_FILE_PATH_FILTERED}"
        )
        if filtered_count > 0:
            import_centralized_sources(OUTPUT_FILE_PATH_FILTERED)
            print("Import done!")
        else:
            print("No resources to import...")
    except Exception as e:
        print("Error...")
        print(e)


if __name__ == "__main__":
    main()
