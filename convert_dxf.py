import sys
import os
import glob
# Dependencies:
# pip install ezdxf matplotlib
import matplotlib.pyplot as plt
import ezdxf
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend

def convert_dxf_to_pdf(input_dir, output_dir):
    # Ensure input directory exists
    if not os.path.exists(input_dir):
        print(f"Error: Input directory '{input_dir}' does not exist.")
        return

    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    # Find all .dxf files in the input directory
    dxf_files = glob.glob(os.path.join(input_dir, "*.dxf"))

    if not dxf_files:
        print(f"No .dxf files found in '{input_dir}'.")
        return

    print(f"Found {len(dxf_files)} .dxf files. Starting conversion...")

    for dxf_file in dxf_files:
        try:
            filename = os.path.basename(dxf_file)
            output_filename = os.path.splitext(filename)[0] + ".pdf"
            output_path = os.path.join(output_dir, output_filename)

            print(f"Converting '{filename}'...")

            doc = ezdxf.readfile(dxf_file)
            msp = doc.modelspace()

            # 1. Create the render context
            ctx = RenderContext(doc)

            # 2. Create the backend
            fig = plt.figure()
            ax = fig.add_axes([0, 0, 1, 1])
            backend = MatplotlibBackend(ax)

            # 3. Create the frontend
            frontend = Frontend(ctx, backend)

            # 4. Draw the layout
            frontend.draw_layout(msp, finalize=True)

            # 5. Save to PDF
            fig.savefig(output_path, dpi=300)
            plt.close(fig)

            print(f"Successfully converted '{filename}' to '{output_filename}'.")

        except IOError:
            print(f"Not a DXF file or a generic I/O error.")
        except ezdxf.DXFStructureError:
            print(f"Invalid or corrupted DXF file.")
        except Exception as e:
            print(f"An error occurred while converting '{filename}': {e}")

if __name__ == "__main__":
    convert_dxf_to_pdf("input", "output")
