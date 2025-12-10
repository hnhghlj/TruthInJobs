#!/usr/bin/env python
"""初始化示例数据脚本"""
import os
import sys
import logging
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'welfare_watch.settings')
django.setup()

from apps.accounts.models import User
from apps.companies.models import Industry, Company
from apps.reviews.models import Review, Comment
from django.contrib.auth import get_user_model

# 配置日志
logger = logging.getLogger('scripts')

User = get_user_model()


def create_users():
    """创建测试用户"""
    logger.info("开始创建用户...")
    
    try:
        # 创建超级管理员
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@welfarewatch.com',
                password='admin123',
                user_type='admin'
            )
            logger.info(f"✓ 创建管理员: {admin.username}")
        else:
            logger.debug("管理员已存在，跳过创建")
        
        # 创建审核员
        if not User.objects.filter(username='moderator').exists():
            moderator = User.objects.create_user(
                username='moderator',
                email='moderator@welfarewatch.com',
                password='moderator123',
                user_type='moderator',
                anonymous_name='审核员小王'
            )
            logger.info(f"✓ 创建审核员: {moderator.username}")
        else:
            logger.debug("审核员已存在，跳过创建")
        
        # 创建普通用户
        normal_users = [
            ('user1', 'user1@example.com', '匿名职场人A'),
            ('user2', 'user2@example.com', '匿名职场人B'),
            ('user3', 'user3@example.com', '匿名职场人C'),
        ]
        
        for username, email, anon_name in normal_users:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password='password123',
                    anonymous_name=anon_name
                )
                logger.info(f"✓ 创建用户: {user.username}")
            else:
                logger.debug(f"用户 {username} 已存在，跳过创建")
        
        logger.info("用户创建完成")
    except Exception as e:
        logger.error(f"创建用户时发生错误: {e}", exc_info=True)
        raise


def create_industries():
    """创建行业分类"""
    logger.info("开始创建行业分类...")
    
    industries_data = [
        ('互联网/IT', '互联网、软件、信息技术服务业'),
        ('金融', '银行、证券、保险、投资等金融服务'),
        ('电子商务', '电商平台、在线零售'),
        ('教育培训', '教育、培训、咨询'),
        ('医疗健康', '医疗、健康、制药'),
        ('制造业', '制造、生产、加工'),
        ('房地产', '房地产开发、物业管理'),
        ('咨询服务', '管理咨询、专业服务'),
        ('广告传媒', '广告、媒体、文化传播'),
        ('消费品', '快消品、零售'),
    ]
    
    try:
        created_count = 0
        for name, desc in industries_data:
            industry, created = Industry.objects.get_or_create(
                name=name,
                defaults={'description': desc}
            )
            if created:
                logger.info(f"✓ 创建行业: {industry.name}")
                created_count += 1
            else:
                logger.debug(f"行业 {name} 已存在，跳过创建")
        
        logger.info(f"行业创建完成，新建 {created_count} 个行业")
    except Exception as e:
        logger.error(f"创建行业时发生错误: {e}", exc_info=True)
        raise


def create_companies():
    """创建示例公司"""
    logger.info("开始创建公司...")
    
    it_industry = Industry.objects.get(name='互联网/IT')
    finance_industry = Industry.objects.get(name='金融')
    ecommerce_industry = Industry.objects.get(name='电子商务')
    
    companies_data = [
        {
            'name': '腾讯',
            'name_en': 'Tencent',
            'industry': it_industry,
            'size': '5001+',
            'founded_year': 1998,
            'location': '广东深圳',
            'website': 'https://www.tencent.com',
            'description': '中国领先的互联网增值服务提供商之一，提供社交、游戏、内容等多元化互联网服务。',
            'is_verified': True
        },
        {
            'name': '阿里巴巴',
            'name_en': 'Alibaba',
            'industry': ecommerce_industry,
            'size': '5001+',
            'founded_year': 1999,
            'location': '浙江杭州',
            'website': 'https://www.alibaba.com',
            'description': '全球领先的电子商务公司，旗下有淘宝、天猫、阿里云等业务。',
            'is_verified': True
        },
        {
            'name': '字节跳动',
            'name_en': 'ByteDance',
            'industry': it_industry,
            'size': '5001+',
            'founded_year': 2012,
            'location': '北京',
            'website': 'https://www.bytedance.com',
            'description': '全球化的移动互联网公司，旗下有抖音、今日头条等产品。',
            'is_verified': True
        },
        {
            'name': '美团',
            'name_en': 'Meituan',
            'industry': it_industry,
            'size': '5001+',
            'founded_year': 2010,
            'location': '北京',
            'website': 'https://www.meituan.com',
            'description': '中国领先的生活服务电子商务平台。',
            'is_verified': True
        },
        {
            'name': '京东',
            'name_en': 'JD.com',
            'industry': ecommerce_industry,
            'size': '5001+',
            'founded_year': 1998,
            'location': '北京',
            'website': 'https://www.jd.com',
            'description': '中国最大的自营式电商企业。',
            'is_verified': True
        },
        {
            'name': '百度',
            'name_en': 'Baidu',
            'industry': it_industry,
            'size': '5001+',
            'founded_year': 2000,
            'location': '北京',
            'website': 'https://www.baidu.com',
            'description': '中国领先的互联网搜索服务提供商，在人工智能领域有深入布局。',
            'is_verified': True
        },
        {
            'name': '华为',
            'name_en': 'Huawei',
            'industry': it_industry,
            'size': '5001+',
            'founded_year': 1987,
            'location': '广东深圳',
            'website': 'https://www.huawei.com',
            'description': '全球领先的ICT基础设施和智能终端提供商。',
            'is_verified': True
        },
        {
            'name': '拼多多',
            'name_en': 'Pinduoduo',
            'industry': ecommerce_industry,
            'size': '1001-5000',
            'founded_year': 2015,
            'location': '上海',
            'website': 'https://www.pinduoduo.com',
            'description': '社交电商平台，专注于C2M拼团购物。',
            'is_verified': True
        },
    ]
    
    try:
        created_companies = []
        created_count = 0
        for data in companies_data:
            company, created = Company.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            created_companies.append(company)
            if created:
                logger.info(f"✓ 创建公司: {company.name}")
                created_count += 1
            else:
                logger.debug(f"公司 {data['name']} 已存在，跳过创建")
        
        logger.info(f"公司创建完成，新建 {created_count} 个公司")
        return created_companies
    except Exception as e:
        logger.error(f"创建公司时发生错误: {e}", exc_info=True)
        raise


def create_reviews(companies):
    """创建示例评价"""
    logger.info("开始创建评价...")
    
    users = User.objects.filter(user_type='normal')
    
    reviews_data = [
        {
            'company': companies[0],  # 腾讯
            'user': users[0],
            'title': '大厂福利确实不错，但加班也是真的多',
            'content': '''
                <h3>工作体验</h3>
                <p>在腾讯工作了两年多，整体感受还是不错的。公司福利待遇在业内属于第一梯队，各种补贴、节日礼品都很到位。</p>
                
                <h3>优点</h3>
                <ul>
                    <li>薪资待遇优厚，年终奖给力</li>
                    <li>办公环境舒适，设施齐全</li>
                    <li>技术氛围浓厚，能学到很多东西</li>
                    <li>团队氛围融洽，同事都很nice</li>
                </ul>
                
                <h3>缺点</h3>
                <ul>
                    <li>加班文化比较严重，基本都是晚上9点后下班</li>
                    <li>项目压力大，经常要赶进度</li>
                    <li>部门之间沟通成本较高</li>
                </ul>
                
                <p>总的来说，如果你想在互联网行业发展，腾讯是个不错的选择。</p>
            ''',
            'overall_rating': 4,
            'welfare_rating': 5,
            'environment_rating': 5,
            'development_rating': 4,
            'management_rating': 3,
            'job_title': '高级前端工程师',
            'employment_status': 'current',
            'work_years': 2,
            'moderation_status': 'approved'
        },
        {
            'company': companies[1],  # 阿里巴巴
            'user': users[1],
            'title': '阿里的工作强度很大，但成长也很快',
            'content': '''
                <h3>整体评价</h3>
                <p>在阿里工作了一年半，这段经历让我成长了很多。阿里的业务体系庞大，能接触到很多有挑战性的项目。</p>
                
                <h3>福利待遇</h3>
                <p>薪资在行业中上水平，股票激励制度不错。五险一金按最高标准缴纳，还有商业保险。</p>
                
                <h3>工作环境</h3>
                <p>园区环境很好，食堂选择多。但是工位比较密集，有时候会觉得有点拥挤。</p>
                
                <h3>发展机会</h3>
                <p>内部晋升机制比较透明，只要业绩好就有机会升职加薪。培训资源丰富。</p>
                
                <h3>需要改进</h3>
                <p>工作强度确实很大，经常996。部门文化差异较大，有的部门氛围很好，有的就比较压抑。</p>
            ''',
            'overall_rating': 4,
            'welfare_rating': 4,
            'environment_rating': 4,
            'development_rating': 5,
            'management_rating': 4,
            'job_title': 'Java开发工程师',
            'employment_status': 'current',
            'work_years': 1,
            'moderation_status': 'approved'
        },
        {
            'company': companies[2],  # 字节跳动
            'user': users[2],
            'title': '年轻有活力的公司，技术驱动',
            'content': '''
                <p>字节跳动是一家非常年轻有活力的公司，平均年龄很小。公司崇尚扁平化管理，层级不多。</p>
                
                <p><strong>薪资福利：</strong>薪资水平在大厂中属于较高的，而且涨薪幅度也不错。</p>
                
                <p><strong>工作氛围：</strong>团队氛围很好，大家都很拼，也很愿意分享。技术栈比较新，能接触到前沿技术。</p>
                
                <p><strong>工作强度：</strong>不得不说工作强度真的很大，基本都是大小周，平时也要加班到很晚。</p>
                
                <p><strong>发展空间：</strong>公司发展很快，机会很多，如果能力强的话晋升速度也快。</p>
            ''',
            'overall_rating': 4,
            'welfare_rating': 5,
            'environment_rating': 4,
            'development_rating': 5,
            'management_rating': 4,
            'job_title': '算法工程师',
            'employment_status': 'current',
            'moderation_status': 'approved'
        },
        {
            'company': companies[0],  # 腾讯
            'user': users[1],
            'title': '作为应届生的第一份工作很满意',
            'content': '''
                <p>作为校招进入腾讯的应届生，这是我的第一份工作。整体来说我很满意。</p>
                
                <p>导师制度很完善，有专门的mentor带我，帮我快速适应公司环境和业务。</p>
                
                <p>团队氛围也很好，同事们都很愿意帮助新人。代码review制度让我学到了很多规范的编码习惯。</p>
                
                <p>薪资待遇对应届生来说很有竞争力，福利也不错。唯一的缺点就是加班比较多。</p>
            ''',
            'overall_rating': 5,
            'welfare_rating': 5,
            'environment_rating': 5,
            'development_rating': 5,
            'management_rating': 5,
            'job_title': '后端开发工程师',
            'employment_status': 'current',
            'moderation_status': 'approved'
        },
    ]
    
    try:
        created_count = 0
        for data in reviews_data:
            review, created = Review.objects.get_or_create(
                company=data['company'],
                user=data['user'],
                title=data['title'],
                defaults=data
            )
            if created:
                logger.info(f"✓ 创建评价: {review.title[:30]}...")
                # 更新公司统计
                review.company.update_statistics()
                created_count += 1
            else:
                logger.debug(f"评价已存在: {data['title'][:30]}")
        
        logger.info(f"评价创建完成，新建 {created_count} 条评价")
    except Exception as e:
        logger.error(f"创建评价时发生错误: {e}", exc_info=True)
        raise


def create_comments():
    """创建示例评论"""
    logger.info("开始创建评论...")
    
    reviews = Review.objects.filter(moderation_status='approved')
    users = User.objects.filter(user_type='normal')
    
    if reviews.exists() and users.exists():
        comments_data = [
            {
                'review': reviews[0],
                'user': users[1],
                'content': '感同身受，我也在腾讯工作，确实加班比较多。不过团队氛围真的很好！',
                'moderation_status': 'approved'
            },
            {
                'review': reviews[0],
                'user': users[2],
                'content': '想问一下，腾讯的年终奖一般是几个月的？',
                'moderation_status': 'approved'
            },
            {
                'review': reviews[1],
                'user': users[0],
                'content': '阿里的工作强度确实很大，但是成长也快，值得！',
                'moderation_status': 'approved'
            },
        ]
        
        try:
            created_count = 0
            for data in comments_data:
                comment, created = Comment.objects.get_or_create(
                    review=data['review'],
                    user=data['user'],
                    content=data['content'],
                    defaults={'moderation_status': data['moderation_status']}
                )
                if created:
                    logger.info(f"✓ 创建评论: {comment.content[:30]}...")
                    created_count += 1
                else:
                    logger.debug(f"评论已存在")
            
            logger.info(f"评论创建完成，新建 {created_count} 条评论")
        except Exception as e:
            logger.error(f"创建评论时发生错误: {e}", exc_info=True)
            raise
    else:
        logger.warning("没有可用的评价或用户，跳过评论创建")


def create_pending_content():
    """创建待审核内容"""
    logger.info("开始创建待审核内容...")
    
    try:
        users = User.objects.filter(user_type='normal')
        companies = Company.objects.all()[:3]
        
        if not users.exists() or not companies.exists():
            logger.warning("没有可用的用户或公司，跳过待审核内容创建")
            return
        
        # 创建待审核评价
        pending_review, created = Review.objects.get_or_create(
            company=companies[0],
            user=users[0],
            title='这是一条待审核的评价',
            defaults={
                'content': '<p>这是测试用的待审核评价内容，需要审核员审核后才能显示。</p>',
                'overall_rating': 4,
                'welfare_rating': 4,
                'environment_rating': 4,
                'development_rating': 4,
                'management_rating': 4,
                'job_title': '测试工程师',
                'moderation_status': 'pending'
            }
        )
        if created:
            logger.info(f"✓ 创建待审核评价: {pending_review.title}")
        else:
            logger.debug("待审核评价已存在")
        
        # 创建待审核评论
        approved_reviews = Review.objects.filter(moderation_status='approved').first()
        if approved_reviews:
            pending_comment, created = Comment.objects.get_or_create(
                review=approved_reviews,
                user=users[0],
                content='这是一条待审核的评论，需要审核员审核。',
                defaults={'moderation_status': 'pending'}
            )
            if created:
                logger.info("✓ 创建待审核评论")
            else:
                logger.debug("待审核评论已存在")
        else:
            logger.warning("没有已审核的评价，跳过待审核评论创建")
        
        logger.info("待审核内容创建完成")
    except Exception as e:
        logger.error(f"创建待审核内容时发生错误: {e}", exc_info=True)
        raise


def main():
    """主函数"""
    logger.info("=" * 60)
    logger.info("WelfareWatch 数据初始化开始")
    logger.info("=" * 60)
    
    try:
        create_users()
        create_industries()
        companies = create_companies()
        create_reviews(companies)
        create_comments()
        create_pending_content()
        
        logger.info("=" * 60)
        logger.info("✅ 数据初始化成功完成！")
        logger.info("=" * 60)
        
        # 输出关键信息到控制台
        print("\n" + "=" * 60)
        print("🎉 数据初始化完成！")
        print("=" * 60)
        print("\n📋 登录信息：")
        print("   管理员账号: admin / admin123")
        print("   审核员账号: moderator / moderator123")
        print("   普通用户: user1 / password123")
        print("   普通用户: user2 / password123")
        print("   普通用户: user3 / password123")
        print("\n🌐 访问地址：")
        print("   后端 API: http://localhost:8000/api/")
        print("   API 文档: http://localhost:8000/api/docs/")
        print("   前端页面: http://localhost:5173/")
        print("=" * 60 + "\n")
        
        logger.info("详细日志已保存到 logs/ 目录")
        
    except Exception as e:
        logger.error("=" * 60)
        logger.error("❌ 数据初始化失败！")
        logger.error("=" * 60)
        logger.error(f"错误信息: {e}", exc_info=True)
        print(f"\n❌ 初始化失败，请查看日志文件: logs/general.log")
        print(f"错误: {e}\n")
        sys.exit(1)


if __name__ == '__main__':
    main()

