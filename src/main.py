# Run the main program
import os
import platform
import zipfile
import shutil

executable_name = "Balatro.exe"
system = platform.system()
file_with_game_speed_code = "functions/UI_definitions.lua"

line_to_replace = "options = {0.5, 1, 2, 4}"


def prompt_game_location():
    game_path = input("Please enter the path to the game executable: ")
    return game_path


def prompt_game_speeds():
    numbers = input("Please enter the speed multipliers you'd like to add, as whole numbers, comma separated.")
    numbers = check_input(numbers)
    if numbers is None:
        print("Invalid input. Please enter whole numbers separated by commas.")
    return numbers


def check_input(numbers: str) -> str | None:
    for number in numbers.split(","):
        if not number.isdigit():
            print(f"Invalid input: {number} is not a whole number.")
            return None
    return numbers


def replace_text_in_zip(zip_folder, file_name, search_text, replace_text):
    # Create a temporary directory to extract files
    temp_dir = f"{zip_folder}/temp_extracted"
    zip_path = f"{zip_folder}/{executable_name}"
    os.makedirs(temp_dir, exist_ok=True)

    # Extract the specified file from the zip archive
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extract(file_name, temp_dir)

    # Path to the extracted file
    extracted_file_path = os.path.join(temp_dir, file_name)

    # Read the file and replace the text
    with open(extracted_file_path, 'r') as file:
        content = file.read()

    modified_content = content.replace(search_text, replace_text)

    # Write the modified content back to the file
    with open(extracted_file_path, 'w') as file:
        file.write(modified_content)

    # Create a new zip file with the modified file
    with zipfile.ZipFile(zip_path, 'a') as zip_ref:
        zip_ref.write(extracted_file_path, file_name)

    # Clean up the temporary directory
    shutil.rmtree(temp_dir)


if __name__ == '__main__':
    game_path = prompt_game_location()
    game_speeds = prompt_game_speeds()
    replacement_text = "options = {0.5, 1, 2, 4," + f"{game_speeds}" + "}"
    line_to_replace = "options = {0.5, 1, 2, 4}"
    replace_text_in_zip(game_path, file_with_game_speed_code, line_to_replace, replacement_text)
