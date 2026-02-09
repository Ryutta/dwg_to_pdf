import os
import subprocess
import glob
import sys

def convert_dwg_to_pdf(input_dir, output_dir):
    # Ensure input directory exists
    if not os.path.exists(input_dir):
        print(f"Error: Input directory '{input_dir}' does not exist.")
        return

    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    # Find all .dwg files in the input directory
    dwg_files = glob.glob(os.path.join(input_dir, "*.dwg"))

    if not dwg_files:
        print(f"No .dwg files found in '{input_dir}'.")
        return

    print(f"Found {len(dwg_files)} .dwg files. Starting conversion with LibreOffice...")

    success_count = 0
    failure_count = 0

    for dwg_file in dwg_files:
        filename = os.path.basename(dwg_file)
        # Output filename logic: LibreOffice automatically uses the input filename base + .pdf
        # We just need to check if the file was created.
        expected_output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + ".pdf")

        print(f"Converting '{filename}'...")

        try:
            # Construct the command
            # libreoffice --headless --convert-to pdf <input_file> --outdir <output_dir>
            # Note: On some systems, you might need to specify the filter explicitly, e.g., pdf:draw_pdf_Export
            cmd = [
                "libreoffice",
                "--headless",
                "--convert-to",
                "pdf",
                dwg_file,
                "--outdir",
                output_dir
            ]

            # Execute the command
            # Using xvfb-run if available on Linux to support headless rendering better
            # Check if xvfb-run is in path
            xvfb = subprocess.run(["which", "xvfb-run"], capture_output=True, text=True).returncode == 0
            if xvfb and sys.platform.startswith("linux"):
                 cmd.insert(0, "xvfb-run")
                 cmd.insert(1, "-a") # Auto server number

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                # Check if file exists
                if os.path.exists(expected_output_path):
                    print(f"Successfully converted '{filename}'.")
                    success_count += 1
                else:
                    print(f"LibreOffice exited successfully but output file '{expected_output_path}' was not found.")
                    print(f"This might mean LibreOffice failed to open the DWG file format.")
                    print(f"Stderr: {result.stderr}")
                    failure_count += 1
            else:
                print(f"Failed to convert '{filename}'.")
                print(f"Error output:\n{result.stderr}")
                failure_count += 1

        except Exception as e:
            print(f"An error occurred while converting '{filename}': {e}")
            failure_count += 1

    print("-" * 30)
    print(f"Conversion complete. Success: {success_count}, Failure: {failure_count}")
    if failure_count > 0:
        print("\nNote: If conversion failed, it might be due to missing DWG import filters in LibreOffice on this system.")
        print("Try installing 'liblibreoffice-java' or using 'ODA File Converter' to convert to DXF first.")

if __name__ == "__main__":
    INPUT_DIR = "input"
    OUTPUT_DIR = "output"
    convert_dwg_to_pdf(INPUT_DIR, OUTPUT_DIR)
