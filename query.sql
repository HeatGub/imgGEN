SELECT * FROM images;
-- SELECT error_types, error_messages FROM images;

-- SELECT * FROM images WHERE error_messages LIKE ('%decode%');

-- SELECT error_types, error_messages FROM images;
-- UPDATE images
-- SET error_messages = COALESCE(error_messages, '') || 'New error message' || char(10) || char(10),
-- error_types = COALESCE(error_types, '') || 'error type' || char(10)
-- WHERE id = 2;


-- SELECT COUNT(*) FROM images WHERE status='processing';
-- SELECT time_proc_start FROM images GROUP BY time_proc_start;

-- SELECT STATUS, COUNT(*) FROM images GROUP BY status;
-- UPDATE images SET status = 'done';
-- UPDATE images SET status = 'pending' WHERE id = 1;


-- SELECT datetime_ FROM images;

-- SELECT time_indexed FROM images GROUP BY time_indexed;

-- SELECT * FROM images WHERE status='processing';
-- SELECT * FROM images WHERE status='done';


-- UPDATE images SET status = 'done' WHERE dir = 'D:\imgGEN\paths\create\generated\000001\000001257617486';
-- SELECT * FROM images WHERE status = 'done';

-- SELECT dir || '\' || file_name AS full_path FROM images;

-- DROP TABLE images;