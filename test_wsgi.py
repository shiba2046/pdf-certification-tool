#!/usr/bin/env python3
"""
测试WSGI设置
Test WSGI setup
"""
import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入应用
from app import app

if __name__ == "__main__":
    print("测试WSGI应用...")
    print("Testing WSGI application...")
    
    # 创建测试客户端
    with app.test_client() as client:
        # 测试主页
        response = client.get('/')
        print(f"主页状态码: {response.status_code}")
        print(f"Homepage status code: {response.status_code}")
        
        if response.status_code == 200:
            print("✓ WSGI应用正常工作")
            print("✓ WSGI application working correctly")
        else:
            print("✗ WSGI应用有问题")
            print("✗ WSGI application has issues")
            
    print("测试完成")
    print("Test complete") 