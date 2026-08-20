import os
import glob
import time

CHATS_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'chats')

class ChatManager:
    @staticmethod
    def _ensure_dir():
        if not os.path.exists(CHATS_DIR):
            os.makedirs(CHATS_DIR)

    @staticmethod
    def get_all_sessions():
        ChatManager._ensure_dir()
        sessions = []
        for filepath in glob.glob(os.path.join(CHATS_DIR, '*.md')):
            session_id = os.path.basename(filepath).replace('.md', '')
            modified_time = os.path.getmtime(filepath)
            
            title = "New Chat"
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    first_line = f.readline().strip()
                    if first_line.startswith('# '):
                        title = first_line[2:]
            except Exception:
                pass
            
            sessions.append({
                "session_id": session_id,
                "title": title,
                "updated_at": modified_time
            })
        
        sessions.sort(key=lambda x: x["updated_at"], reverse=True)
        return sessions

    @staticmethod
    def get_session_history(session_id: str):
        filepath = os.path.join(CHATS_DIR, f"{session_id}.md")
        if not os.path.exists(filepath):
            return []
            
        history = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            parts = content.split("### **")
            for part in parts[1:]:
                # Split the sender and the message
                lines = part.split('**', 1)
                if len(lines) < 2:
                    continue
                
                sender = lines[0].strip()
                message = lines[1].strip()
                
                is_user = (sender == "ME")
                history.append({
                    "is_user": is_user,
                    "agent": None if is_user else sender,
                    "content": message
                })
        except Exception:
            pass
            
        return history

    @staticmethod
    def save_turn(session_id: str, user_prompt: str, agent_name: str, agent_response: str):
        ChatManager._ensure_dir()
        filepath = os.path.join(CHATS_DIR, f"{session_id}.md")
        
        is_new = not os.path.exists(filepath)
        
        with open(filepath, 'a', encoding='utf-8') as f:
            if is_new:
                # Generate title from first prompt
                title_text = user_prompt.replace('\n', ' ')
                title = title_text[:30] + ("..." if len(title_text) > 30 else "")
                f.write(f"# {title}\n\n")
                
            f.write(f"### **ME**\n{user_prompt}\n\n")
            f.write(f"### **{agent_name}**\n{agent_response}\n\n")
