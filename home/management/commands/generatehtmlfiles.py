import os
import re
import logging
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)

def views_source_code():
    try:
        views_path = 'C:\\Users\\Dell\\Desktop\\Net_Result\\django-material-dashboard\\home\\views.py'
        with open(views_path, 'r') as file:
            views_source_code = file.read()
        return views_source_code
    except FileNotFoundError:
        logger.error("Views source code file not found.")
        return ""

def extract_all_html_templates(views_code_as_a_string):
    try:
        html_file_pattern = r'(?:"|\'|loader\.get_template\()([^"\']+\.html)(?:"|\'|\))|(?:"|\'|render\(request, )("[^"]+\.html)(?:"|\'|,)'
        html_file_matches = re.findall(html_file_pattern, views_code_as_a_string)
        cleaned_html_files = []

        for match in html_file_matches:
            for item in match:
                if item:
                    cleaned_file_name = item.strip('"\'')
                    cleaned_html_files.append(cleaned_file_name)

        final_cleaned_html_files = [re.sub(r'^[^/]+/', '', item) for item in cleaned_html_files]
        return final_cleaned_html_files
    except Exception as e:
        logger.error(f"Error while extracting HTML templates: {str(e)}")
        return []

def create_html_files(required_html_files):
    num_files_created = 0  # Initialize a counter
    new_html_files = []
    try: 
        output_directory = 'C:\\Users\\Dell\\Desktop\\Net_Result\\django-material-dashboard\\templates\\home\\'

        for filename in required_html_files:
            # Construct the full file path
            full_path = os.path.join(output_directory, filename)

            # Check if the file already exists
            if os.path.exists(full_path):
                logger.warning(f"File '{filename}' already exists. Skipping.")
            else:
                # Write the file if it doesn't exist
                with open(full_path, 'w') as file:
                    # You can customize the content as needed
                    file.write("{% extends 'layouts/base.html' %} {% block title %} Tables {% endblock title %} {% block content %} <div style=""></div>{%endblock%}")
                    new_html_files.append(full_path)

                num_files_created += 1  # Increment the counter

                logger.info(f"File '{filename}' created successfully.")
    except Exception as e:
        logger.error(f"Error while creating HTML files: {str(e)}")

    return f"{num_files_created} number of HTML files generated in {output_directory}. The paths are {new_html_files}"

class Command(BaseCommand):
    help = 'Generate HTML files from view templates'

    def handle(self, *args, **kwargs):
        try:
            output_directory = 'C:\\Users\\Dell\\Desktop\\Net_Result\\django-material-dashboard\\templates\\home\\'
            result_message = create_html_files(extract_all_html_templates(views_source_code()))
            self.stdout.write(self.style.SUCCESS(result_message))
        except Exception as e:
            logger.error(f"Command execution error: {str(e)}")