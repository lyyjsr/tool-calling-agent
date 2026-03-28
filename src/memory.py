from src.schemas import MessageRecord

class ConversationMemory:
    def __init__(self,max_records:int =5):
        self.max_records = max_records
        self.records:list[MessageRecord] = []

    def add_record(self,record:MessageRecord)->None:
        self.records.append(record)
        if len(self.records) > self.max_records:
            self.records.pop(0)

    def get_records(self)->list[MessageRecord]:
        return self.records

    def format_history(self)->str:
        if not self.records:
            return "当前还没有会话历史。"
        lines = ["最近会话历史:"]
        for index,record in enumerate(self.records,start=1):
            lines.append(f"{index}.用户：{record.user_input}")
            lines.append(f"  意图：{record.intent}")
            lines.append(f"  回复：{record.response}")
        return "\n".join(lines)
