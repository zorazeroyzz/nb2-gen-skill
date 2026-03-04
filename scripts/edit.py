#!/usr/bin/env python3
"""NB2 图片编辑（二次元转真人等）"""
import argparse, sys
from nb2_utils import get_config, call_api, save_image, make_image_content, make_text_content

def main():
    parser = argparse.ArgumentParser(description="NB2 图片编辑")
    parser.add_argument("input", help="输入图片路径")
    parser.add_argument("prompt", help="编辑指令（如：把这张图变成真人coser）")
    parser.add_argument("output", help="输出图片路径")
    parser.add_argument("--temp", type=float, default=0.8, help="temperature (默认0.8)")
    parser.add_argument("--model", default=None, help="覆盖模型名")
    args = parser.parse_args()

    cfg = get_config()
    if args.model:
        cfg["model"] = args.model

    # Image first, then text - best for editing
    messages = [{"role": "user", "content": [
        make_image_content(args.input),
        make_text_content(args.prompt)
    ]}]

    print(f"Editing: {args.input}")
    print(f"Prompt: {args.prompt}")
    
    img_bytes, err = call_api(messages, cfg, temperature=args.temp)
    if img_bytes:
        save_image(img_bytes, args.output)
    else:
        print(f"Failed: {err}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
