#!/usr/bin/env python3
"""NB2 多图合成"""
import argparse, sys
from nb2_utils import get_config, call_api, save_image, make_image_content, make_text_content

def main():
    parser = argparse.ArgumentParser(description="NB2 多图合成（最多14张）")
    parser.add_argument("prompt", help="合成指令（如：图1的人摆图2的姿势）")
    parser.add_argument("output", help="输出图片路径")
    parser.add_argument("images", nargs="+", help="输入图片路径（1-14张）")
    parser.add_argument("--temp", type=float, default=0.8, help="temperature (默认0.8)")
    parser.add_argument("--model", default=None, help="覆盖模型名")
    args = parser.parse_args()

    if len(args.images) > 14:
        print("Error: 最多支持14张图片", file=sys.stderr)
        sys.exit(1)

    cfg = get_config()
    if args.model:
        cfg["model"] = args.model

    # Build content: images first, then prompt
    content = []
    for img_path in args.images:
        content.append(make_image_content(img_path))
    content.append(make_text_content(args.prompt))

    messages = [{"role": "user", "content": content}]

    print(f"Composing {len(args.images)} images")
    print(f"Prompt: {args.prompt}")
    
    img_bytes, err = call_api(messages, cfg, temperature=args.temp)
    if img_bytes:
        save_image(img_bytes, args.output)
    else:
        print(f"Failed: {err}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
