# PDF Scraper

A Python-based web scraper for downloading PDF files from web pages with customizable filtering options. This tool is particularly useful for bulk downloading course materials, academic papers, or any collection of PDFs from a website.

## Features

- 🔍 **Pattern Matching**: Automatically finds and downloads PDFs matching specific URL patterns
- 🚫 **Smart Filtering**: Skip files based on customizable restriction patterns (e.g., exclude "plenum", "oving" files)
- 📁 **Organized Downloads**: Saves files to a specified directory with automatic duplicate handling
- 🛡️ **Error Handling**: Gracefully handles download failures and continues with remaining files
- 🔄 **Duplicate Prevention**: Automatically renames files if they already exist

## Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

## Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd pdf_scrapper
```

2. Create a virtual environment (recommended):
```bash
python -m venv .venv
```

3. Activate the virtual environment:
   - **Windows**:
     ```bash
     .venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     source .venv/bin/activate
     ```

4. Install required dependencies:
```bash
pip install requests beautifulsoup4
```

## Usage

### Basic Usage

Download all matching PDFs from a webpage:

```bash
python math_pdf_scrapper.py <URL>
```

### Specify Output Directory

```bash
python math_pdf_scrapper.py <URL> -o <output_directory>
```

### Examples

```bash
# Download to default 'downloads' folder
python math_pdf_scrapper.py https://example.com/course-materials

# Download to custom folder
python math_pdf_scrapper.py https://example.com/course-materials -o my_pdfs
```

## Configuration

### Target Pattern

By default, the scraper looks for PDFs matching the pattern `/_media/*.pdf`. You can modify this in the code:

```python
TARGET_PATTERN = re.compile(r"/_media/.*\.pdf$", re.IGNORECASE)
```

### Restricted Patterns

Customize which files to skip by editing the `RESTRICTED_PATTERNS` list:

```python
RESTRICTED_PATTERNS = [
    re.compile(r"plenum", re.IGNORECASE),
    re.compile(r"lf-plenum", re.IGNORECASE),
    re.compile(r"oving", re.IGNORECASE),
    # Add your own patterns here
]
```

## How It Works

1. **Fetch Page**: The script fetches the HTML content from the provided URL
2. **Find Links**: Parses all `<a>` tags and extracts PDF links matching the target pattern
3. **Filter**: Applies restriction patterns to exclude unwanted files
4. **Download**: Downloads each PDF to the specified output directory
5. **Handle Duplicates**: If a file already exists, appends a counter to the filename

## Command-Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `url` | Page URL to scan for PDF links | Required |
| `-o, --output-dir` | Directory to save downloaded files | `downloads` |

## Error Handling

- If a download fails, the script logs the error and continues with remaining files
- Network errors and HTTP errors are caught and reported
- The script exits gracefully if no matching links are found

## Example Output

```
[+] Fetching page: https://example.com/course-materials
[+] Found 15 matching links (before restriction filter)
[!] Skipping restricted file: plenum_2024.pdf
[+] Downloading https://example.com/_media/lecture01.pdf -> downloads/lecture01.pdf
[+] Done: downloads/lecture01.pdf
[+] Downloading https://example.com/_media/lecture02.pdf -> downloads/lecture02.pdf
[+] Done: downloads/lecture02.pdf
...
```

## Dependencies

- **requests**: For making HTTP requests
- **beautifulsoup4**: For parsing HTML content

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'requests'`
- **Solution**: Install dependencies with `pip install requests beautifulsoup4`

**Issue**: Permission denied when creating output directory
- **Solution**: Ensure you have write permissions in the target directory

**Issue**: No PDFs found
- **Solution**: Check that the target URL contains links matching the `TARGET_PATTERN`

## Notes

- This tool respects the website's structure and downloads only publicly accessible PDFs
- Be mindful of the website's terms of service and robots.txt
- Consider adding delays between downloads for large batches to avoid overwhelming the server

## Author

Created for downloading course materials and academic resources efficiently.

---

**Disclaimer**: Use this tool responsibly and ensure you have permission to download content from the target website.
