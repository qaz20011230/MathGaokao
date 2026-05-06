CREATE TABLE IF NOT EXISTS documents (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(500) NOT NULL COMMENT '文档标题',
    `year` INT NOT NULL COMMENT '年份，1905-2025',
    period ENUM('pre_1952', '1952_1965', '1977_now') NOT NULL COMMENT '时期',
    doc_type ENUM('exam_paper', 'answer_sheet', 'answer_key', 'other') NOT NULL COMMENT '文档类型',
    province VARCHAR(50) DEFAULT NULL COMMENT '省份或高校名称',
    exam_category VARCHAR(50) DEFAULT NULL COMMENT '理科/文科/新高考',
    file_path VARCHAR(500) NOT NULL COMMENT '文件存储路径',
    file_format ENUM('pdf', 'image') NOT NULL DEFAULT 'pdf',
    file_size BIGINT DEFAULT 0 COMMENT '文件大小(字节)',
    file_md5 VARCHAR(32) DEFAULT NULL COMMENT '文件MD5',
    page_count INT DEFAULT NULL COMMENT '页数',
    description TEXT COMMENT '文档描述',
    source VARCHAR(200) DEFAULT NULL COMMENT '来源标注',
    year_title VARCHAR(100) DEFAULT NULL COMMENT '早期资料用高校名代替年份标题',
    is_published TINYINT(1) DEFAULT 1 COMMENT '是否发布',
    download_count INT DEFAULT 0 COMMENT '下载次数',
    view_count INT DEFAULT 0 COMMENT '浏览次数',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    UNIQUE KEY uk_document (year, province, doc_type, exam_category),
    INDEX idx_year (year),
    INDEX idx_period (period),
    INDEX idx_doc_type (doc_type),
    INDEX idx_province (province),
    FULLTEXT INDEX ft_title_desc (title, description)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='高考数学文档';

CREATE TABLE IF NOT EXISTS admins (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='管理员表';
