# main.py
import argparse
from postgenerator import run_post
from respondgenerator import run_reply

def main():
    parser = argparse.ArgumentParser(description="🧠 Flarum 自动发帖/回帖工具")
    subparsers = parser.add_subparsers(dest="command", help="选择功能")

    # 发主贴
    post_parser = subparsers.add_parser("post", help="生成并发布主贴")
    post_parser.add_argument("--keyword", type=str, required=True, help="语义搜索关键词")

    # 回帖子
    reply_parser = subparsers.add_parser("reply", help="根据贴子 ID 回帖")
    reply_parser.add_argument("--id", type=int, required=True, help="讨论帖 discussion ID")
    reply_parser.add_argument("--num", type=int, default=3, help="生成回复数量（默认3）")

    args = parser.parse_args()

    if args.command == "post":
        print(f"📝 生成并发帖，关键词：{args.keyword}")
        run_post(args.keyword)

    elif args.command == "reply":
        print(f"💬 回帖模式，帖子 ID：{args.id}，回复数量：{args.num}")
        run_reply(discussion_id=args.id, num_replies=args.num)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
