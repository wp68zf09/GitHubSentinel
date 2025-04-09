# src/github_client.py

import requests  # 导入requests库用于HTTP请求
from datetime import datetime, date, timedelta  # 导入日期处理模块
import os  # 导入os模块用于文件和目录操作
from logger import LOG  # 导入日志模块
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class CnblogsClient:     
    def export_progress_crawler(self):
        url = 'https://www.cnblogs.com/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    
        soup = BeautifulSoup(response.text, 'html.parser')
        title_tags = soup.find_all('a', class_='post-item-title')
    
        # 提取并处理前5条数据
        top_stories = []
        for tag in title_tags[:5]:  # 取前5条
            title = tag.text.strip()
            link = urljoin(url, tag['href'])
            
            # 提取摘要
            summary_tag = tag.find_next('p', class_='post-item-summary')
            summary = summary_tag.text.strip() if summary_tag else ""
            
            # 智能截取
            max_title_len = 25
            max_summary_len = 100
            formatted_title = (title[:max_title_len] + '...') if len(title) > max_title_len else title
            formatted_summary = (summary[:max_summary_len] + '...') if len(summary) > max_summary_len else summary
            
            top_stories.append({
                'title': formatted_title,
                'summary': formatted_summary,
                'link': link
            })
    
        return self.format_stories_to_string(top_stories)
    def format_stories_to_string(self,stories):
        """将文章列表格式化为易读的字符串"""
        if not stories:
            return "未找到热门文章"
        
        formatted_str = "博客园热门文章TOP5：\n\n"
        
        for idx, story in enumerate(stories, 1):
            # 添加序号
            formatted_str += f"{idx}. 📌 {story['title']}\n"
            
            # 添加摘要
            formatted_str += f"   📖 {story['summary']}\n"
            
            # 添加链接
            formatted_str += f"   🔗 {story['link']}\n\n"
            
            # 添加分隔线
            if idx < len(stories):
                formatted_str += "------------------------------------\n"
        
        return formatted_str