# CLI-difycall
# Dify Chat CLI Tool

A simple command line tool to chat with different Dify AI platforms.

## How to Use

Basic usage:
```bash
python main.py -p <platform> -m "your message"
```

## Options

- `-p` or `--platform`: Choose the AI platform (required)
- `-m` or `--message`: Your message to send (required)
- `-c` or `--conversation-id`: Keep chat history with same ID (optional)

## Examples

1. Simple chat:
```bash
python main.py -p wechat -m "Hello, what's the weather?"
```

2. Continue a conversation:
```bash
# First message
python main.py -p wechat -m "Who was Albert Einstein?" -c "chat123"

# Follow-up question (using same conversation-id)
python main.py -p wechat -m "What were his main achievements?" -c "chat123"
```

The conversation-id helps you:
- Continue previous chats
- Keep context between messages
- Get better follow-up answers

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