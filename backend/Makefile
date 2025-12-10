.PHONY: help install migrate test lint format clean run

help:  ## 显示帮助信息
	@echo "WelfareWatch 后端管理命令"
	@echo ""
	@echo "使用方法: make [命令]"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## 安装依赖
	pip install -r requirements.txt

migrate:  ## 执行数据库迁移
	python manage.py makemigrations
	python manage.py migrate

test:  ## 运行测试
	pytest

test-cov:  ## 运行测试并生成覆盖率报告
	pytest --cov --cov-report=html --cov-report=term

lint:  ## 代码检查
	flake8 apps utils
	mypy apps utils

format:  ## 代码格式化
	black apps utils config
	isort apps utils config

clean:  ## 清理临时文件
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '*.egg-info' -exec rm -rf {} +
	rm -rf htmlcov .coverage .pytest_cache

run:  ## 运行开发服务器
	python manage.py runserver

shell:  ## 进入Django Shell
	python manage.py shell_plus --ipython

check:  ## 检查项目配置
	python manage.py check

collectstatic:  ## 收集静态文件
	python manage.py collectstatic --noinput

init-data:  ## 初始化示例数据
	python init_data.py

logs:  ## 查看日志
	python view_logs.py general.log

logs-error:  ## 查看错误日志
	python view_logs.py error.log

analyze:  ## 分析日志
	python analyze_logs.py

backup-db:  ## 备份数据库
	mysqldump -u root -p welfarewatch > backup_$$(date +%Y%m%d_%H%M%S).sql

all: clean install migrate test  ## 完整安装流程

