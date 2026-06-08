import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os


# 数据文件
DATA_FILE = "../data/豆瓣电影Top250.csv"


class MovieGUI:
    """
    豆瓣Top250电影查询系统
    """

    def __init__(self, root):
        self.root = root
        self.root.title("豆瓣Top250电影查询系统")
        self.root.geometry("1100x650")

        self.df = pd.DataFrame()

        # =====================
        # 顶部功能区
        # =====================
        top_frame = tk.Frame(root)
        top_frame.pack(pady=10)

        tk.Label(
            top_frame,
            text="电影名称：",
            font=("微软雅黑", 10)
        ).pack(side=tk.LEFT)

        self.search_var = tk.StringVar()

        tk.Entry(
            top_frame,
            textvariable=self.search_var,
            width=30
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            top_frame,
            text="搜索",
            command=self.search_movie
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            top_frame,
            text="显示全部",
            command=self.load_data
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            top_frame,
            text="按评分排序",
            command=self.sort_score
        ).pack(side=tk.LEFT, padx=5)

        # =====================
        # 表格区域
        # =====================
        table_frame = tk.Frame(root)
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = (
            "排名",
            "电影名",
            "评分",
            "信息",
            "类型"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        self.tree.heading("排名", text="排名")
        self.tree.heading("电影名", text="电影名")
        self.tree.heading("评分", text="评分")
        self.tree.heading("信息", text="导演/主演信息")
        self.tree.heading("类型", text="类型")

        self.tree.column("排名", width=60, anchor="center")
        self.tree.column("电影名", width=220)
        self.tree.column("评分", width=80, anchor="center")
        self.tree.column("信息", width=500)
        self.tree.column("类型", width=200)

        self.tree.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True
        )

        # 滚动条
        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        scrollbar.pack(
            side=tk.RIGHT,
            fill=tk.Y
        )

        # 双击查看详情
        self.tree.bind(
            "<Double-1>",
            self.show_detail
        )

        # 加载数据
        self.load_data()

    # ==================================
    # 加载CSV数据
    # ==================================
    def load_data(self):
        """
        加载CSV文件
        """

        try:
            self.df = pd.read_csv(DATA_FILE)

        except FileNotFoundError:
            messagebox.showerror(
                "错误",
                f"未找到文件：{DATA_FILE}"
            )
            return

        except Exception as e:
            messagebox.showerror(
                "错误",
                str(e)
            )
            return

        self.refresh_table(self.df)

    # ==================================
    # 刷新表格
    # ==================================
    def refresh_table(self, dataframe):
        """
        更新表格内容
        """

        for item in self.tree.get_children():
            self.tree.delete(item)

        for index, row in dataframe.iterrows():

            movie_name = row.get("电影名", "")
            score = row.get("评分", "")
            info = row.get("信息", "")
            genre = row.get("类型(genres)", "")

            self.tree.insert(
                "",
                tk.END,
                values=(
                    index + 1,
                    movie_name,
                    score,
                    info,
                    genre
                )
            )

    # ==================================
    # 搜索电影
    # ==================================
    def search_movie(self):
        """
        根据电影名称搜索
        """

        keyword = self.search_var.get().strip()

        if keyword == "":
            self.refresh_table(self.df)
            return

        result = self.df[
            self.df["电影名"]
            .astype(str)
            .str.contains(keyword, na=False)
        ]

        self.refresh_table(result)

    # ==================================
    # 按评分排序
    # ==================================
    def sort_score(self):
        """
        按评分降序排列
        """

        sorted_df = self.df.sort_values(
            by="评分",
            ascending=False
        )

        self.refresh_table(sorted_df)

    # ==================================
    # 双击显示详情
    # ==================================
    def show_detail(self, event):

        selected = self.tree.selection()

        if not selected:
            return

        values = self.tree.item(
            selected[0]
        )["values"]

        messagebox.showinfo(
            "电影详情",
            f"排名：{values[0]}\n\n"
            f"电影名：{values[1]}\n\n"
            f"评分：{values[2]}\n\n"
            f"导演/主演信息：\n{values[3]}\n\n"
            f"电影类型：{values[4]}"
        )


# ==========================
# 程序入口
# ==========================
if __name__ == "__main__":

    root = tk.Tk()

    app = MovieGUI(root)

    root.mainloop()