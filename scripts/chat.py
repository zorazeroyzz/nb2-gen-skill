#!/usr/bin/env python3
"""NB2 多轮对话迭代"""
import sys, os
from nb2_utils import get_config, call_api, save_image, make_image_content, make_text_content

def main():
    cfg = get_config()
    messages = []
    
    print("NB2 多轮对话模式")
    print("命令: /load <图片> | /save <路径> | /undo | /clear | /quit")
    print("-" * 50)
    
    while True:
        try:
            user_input = input("\n你: ").strip()
            
            if not user_input:
                continue
                
            if user_input == "/quit":
                break
                
            if user_input == "/clear":
                messages = []
                print("对话已清空")
                continue
                
            if user_input == "/undo":
                if messages:
                    messages.pop()
                    print("已撤销上一轮")
                else:
                    print("没有可撤销的内容")
                continue
                
            if user_input.startswith("/load "):
                img_path = user_input[6:].strip()
                if os.path.exists(img_path):
                    messages.append({"role": "user", "content": [make_image_content(img_path)]})
                    print(f"已加载图片: {img_path}")
                else:
                    print(f"图片不存在: {img_path}")
                continue
                
            if user_input.startswith("/save "):
                output_path = user_input[6:].strip()
                print("使用 /save 前需要先进行一次生成")
                continue
            
            # Regular prompt
            content = []
            
            # Check if last message was an image load
            if messages and messages[-1]["role"] == "user":
                last_content = messages[-1]["content"]
                if isinstance(last_content, list) and len(last_content) == 1:
                    if last_content[0].get("type") == "image_url":
                        # Use the loaded image
                        content = last_content.copy()
                        content.append(make_text_content(user_input))
                        messages[-1] = {"role": "user", "content": content}
                        print("将结合已加载的图片和当前提示词")
                        continue
            
            # New text message
            content = [make_text_content(user_input)]
            messages.append({"role": "user", "content": content})
            
            print("生成中...")
            img_bytes, err = call_api(messages, cfg)
            
            if img_bytes:
                # Save to temp and show
                temp_path = "/tmp/nb2_chat_last.jpg"
                save_image(img_bytes, temp_path)
                messages.append({"role": "assistant", "content": [{"type": "image_url", "image_url": {"url": f"file://{temp_path}"}}]})
                print(f"已生成: {temp_path}")
                print("提示: 使用 /save <路径> 保存，或直接继续输入修改意见")
            else:
                print(f"生成失败: {err}")
                messages.pop()  # Remove failed prompt
                
        except KeyboardInterrupt:
            print("\n再见!")
            break
        except Exception as e:
            print(f"错误: {e}")

if __name__ == "__main__":
    main()
