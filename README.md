# CLI-difycall 
CLI-difycall is a simple command line tool to chat with different Dify AI platforms.

## Setup

1. Install requirements:
```bash
pip install -r requirements.txt
```

2. Configure your Dify API:
- Copy `config.example.py` to `config.py`
- Add your Dify API endpoints and keys in `config.py`

3. Fix SSL warning (if you see urllib3 SSL warning):
```bash
# Option 1: Downgrade urllib3
pip install urllib3==1.26.6

# Option 2: Upgrade OpenSSL (on Mac)
brew install openssl@1.1
```

## How to Use

Basic usage:
```bash
python main.py -p <platform> -m "your message"
```

## Options

- `-p` or `--platform`: Choose the AI platform (required)
- `-m` or `--message`: Your message to send (required)

## Examples

Simple chat:
```bash
python main.py -p wechat -m "Hello, what's the weather?"
```

## Available Platforms

You can use these platforms:
- wechat
- telegram
- (other platforms from your config)

## Error Messages

If something goes wrong, you will see:
- Wrong platform error
- Connection error
- Other error messages

## Need Help?

Run this to see all options:
```bash
python main.py --help
```

## Troubleshooting

If you see "400 BAD REQUEST" error:
1. Check if your Dify API service is running
2. Verify your API endpoints in config.py
3. Make sure your platform configuration is correct
4. Check if your API key is valid

Common issues:
- API service not running (check if http://127.0.0.1 is correct)
- Wrong API endpoint
- Invalid API key
- Platform not properly configured

SSL/TLS Issues:
- If you see urllib3 SSL warning, you can:
  1. Downgrade urllib3: `pip install urllib3==1.26.6`
  2. Upgrade OpenSSL (recommended for Mac users): `brew install openssl@1.1`
  3. Ignore the warning if everything works fine