
# Wiki to JSON Converter

![image](https://github.com/user-attachments/assets/df0e7c49-73f0-4ffa-bc8b-02eed2d11495)

A Python GUI tool to fetch tables from a Wikipedia page and save them as a JSON file.

## Features

- Fetch tables from any Wikipedia URL.
- Clean column names and convert data to JSON format.
- User-friendly interface with `tkinter`.
- Separate CLI version also included.

## Installation

1. Clone the repository and enter its directory:
   ```bash
   git clone https://github.com/your-username/wiki-to-json.git && cd wiki-to-json
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install `tkinter` on Ubuntu (if not already installed):
   ```bash
   sudo apt update
   sudo apt install python3-tk
   ```

## Inspiration and Credits

This project is inspired by [GPU Info API](https://github.com/voidful/gpu-info-api).

## Usage

### GUI

Run the script:

```bash
python wiki-to-json.py
```

### CLI

```bash
python wiki-to-json-cli.py
```

Follow the instructions in the GUI to enter a URL and save the JSON file. For the CLI, you need to run it in a terminal and paste the Wiki link.



## License

This project is licensed under the MIT License.
