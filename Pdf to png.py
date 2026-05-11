import os
from pathlib import Path
import fitz  # PyMuPDF library

def convert_pdfs_to_pngs():
    # 1. Ask the user for the source folder path
    source_path_str = input("Please enter the folder path containing the PDFs: ").strip()
    
    # Strip quotes in case the user dragged and dropped the folder into the terminal
    if source_path_str.startswith(('"', "'")) and source_path_str.endswith(('"', "'")):
        source_path_str = source_path_str[1:-1]
        
    source_dir = Path(source_path_str)

    # Validate if the directory exists
    if not source_dir.is_dir():
        print(f"\n[Error] The directory '{source_dir}' does not exist.")
        return

    # 2. Create the target directory at the same level as the chosen folder
    # Example: If source is 'C:/Documents/Invoices', target becomes 'C:/Documents/Invoices_PNGs'
    target_dir = source_dir.parent / f"{source_dir.name}_PNGs"
    target_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\nTarget directory created at: {target_dir}")
    print("-" * 50)

    # 3. Find all PDFs in the source folder and its subfolders
    # We check for both lowercase and uppercase extensions
    pdf_files = list(source_dir.rglob("*.pdf")) + list(source_dir.rglob("*.PDF"))
    
    if not pdf_files:
        print("[Warning] No PDF files found in the specified directory or its subfolders.")
        return

    # 4. Process each PDF file
    for pdf_path in pdf_files:
        # Calculate the relative path to maintain the exact subfolder structure
        rel_path = pdf_path.parent.relative_to(source_dir)
        
        # Create the corresponding subfolder inside the new target directory
        output_subfolder = target_dir / rel_path
        output_subfolder.mkdir(parents=True, exist_ok=True)
        
        print(f"Processing: {pdf_path.name} ...")
        
        try:
            # Open the PDF document
            pdf_document = fitz.open(pdf_path)
            
            # Iterate through each page (PDFs can have multiple pages)
            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                
                # Extract the page as an image (dpi=300 ensures high resolution)
                pix = page.get_pixmap(dpi=300)
                
                # Create the output filename (e.g., filename_page_1.png)
                base_name = pdf_path.stem
                output_file = output_subfolder / f"{base_name}_page_{page_num + 1}.png"
                
                # Save the image
                pix.save(str(output_file))
                
            pdf_document.close()
            
        except Exception as e:
            print(f"[Error] Failed to process {pdf_path.name}: {e}")

    print("-" * 50)
    print(f"Conversion complete! All PNGs have been saved to:\n{target_dir}")

if __name__ == "__main__":
    convert_pdfs_to_pngs()