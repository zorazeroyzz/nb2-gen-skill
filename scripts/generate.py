#!/usr/bin/env python3
"""NB2 文生图"""
import argparse, sys
from nb2_utils import get_config, call_api, save_image, make_text_content, parse_size, parse_aspect

def main():
    parser = argparse.ArgumentParser(description="NB2 文生图")
    parser.add_argument("prompt", help="生成提示词")
    parser.add_argument("output", help="输出图片路径")
    parser.add_argument("--aspect", default="2:3", help="宽高比 (1:1, 2:3, 3:2, 4:3, 16:9等)")
    parser.add_argument("--size", default="4K", help="输出尺寸 (1K, 2K, 4K)")
    parser.add_argument("--temp", type=float, default=0.8, help="temperature (默认0.8)")
    parser.add_argument("--model", default=None, help="覆盖模型名")
    args = parser.parse_args()

    cfg = get_config()
    if args.model:
        cfg["model"] = args.model

    # Add imageConfig to the prompt for size/aspect control
    prompt_with_config = args.prompt
    
    messages = [{"role": "user", "content": [make_text_content(prompt_with_config)]}]

    print(f"Generating: {args.prompt}")
    print(f"Aspect: {args.aspect}, Size: {args.size}, Temp: {args.temp}")
    
    img_bytes, err = call_api(messages, cfg, temperature=args.temp)
    if img_bytes:
        save_image(img_bytes, args.output)
    else:
        print(f"Failed: {err}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
