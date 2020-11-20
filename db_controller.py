import sqlite3


class db_controller:
    def __init__(self):
        self.db = sqlite3.connect('govno.db')
        self.cursor = self.db.cursor()

    def addNote(self, id, text, status):
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS \'{id}\'(text TEXT, message_status TEXT)")
        self.db.commit()
        self.cursor.execute(f"INSERT INTO \'{id}\' VALUES(\'{text}\', \'{status}\')")
        self.db.commit()

    def showAll(self, id):
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS \'{id}\'(text TEXT, message_status TEXT)")
        self.cursor.execute(f"SELECT text, message_status FROM \'{id}\'")
        tmp = self.cursor.fetchall()
        res_string = ''
        for i in range(0, len(tmp)):
            res_string += f"{i + 1}){tmp[i][0]} [{tmp[i][1]}]\n"
        return res_string

    def DelItem(self, chat_id):
        try:
            self.cursor.execute(f"SELECT text, message_status FROM \'{chat_id.from_user.id}\'")
            tmp = self.cursor.fetchall()
            tmp = tmp[int(chat_id.text) - 1]
            self.cursor.execute(
                f"DELETE FROM \'{chat_id.from_user.id}\' WHERE text=\'{tmp[0]}\' AND message_status=\'{tmp[1]}\'")
            self.db.commit()
        except:
            pass

    def ChangeStatus(self, chat_id):
        try:
            self.cursor.execute(f"SELECT text, message_status FROM \'{chat_id.from_user.id}\'")
            tmp = self.cursor.fetchall()
            tmp = tmp[int(chat_id.text) - 1]
            if tmp[1] == 'active':
                status = 'complete'
            else:
                status = 'active'
            self.cursor.execute(f'UPDATE \'{chat_id.from_user.id}\' SET message_status=\'{status}\' WHERE text=\'{tmp[0]}\' AND message_status=\'{tmp[1]}\'')
            self.db.commit()
        except:
            pass

    def ChangeText(self, num, text, id):
        try:
            num = int(num)
            self.cursor.execute(f"SELECT text, message_status FROM \'{id}\'")
            tmp = self.cursor.fetchall()
            tmp = tmp[num - 1]
            self.cursor.execute(f"UPDATE \'{id}\' SET text=\'{text}\' WHERE text=\'{tmp[0]}\' AND message_status=\'{tmp[1]}\'")
            self.db.commit()
        except:
            pass
