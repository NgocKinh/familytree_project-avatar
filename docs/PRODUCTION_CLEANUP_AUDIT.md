# Production Cleanup Audit

| File | Status | Evidence |
|---|---|---|
| backend/api/clean_parent_api_old.py | READY FOR DELETE | Không import; không router; không frontend gọi |
| backend/app.py | READY FOR DELETE | Flask legacy; Production dùng backend/main.py; hardcode DB localhost |
| backend/run_patch.bat | VERIFY | Cần kiểm tra patch_production_idempotent.sql còn dùng không |
| backend/api/gene_propagate.py | KEEP | backend/services/parent_child_service.py đang import |
| backend/db_helper.py | KEEP | backend/api/person.py đang sử dụng |
| backend/tsconfig.json | VERIFY | Tham chiếu backend/src/**/*; cần xác minh còn dùng |
| backend/src/relations/* | VERIFY | Có nhiều file JS/TS; cần xác minh còn được Production sử dụng |
| backend/src/relations/* | READY FOR DELETE | Backend/Frontend không tham chiếu trực tiếp; relationship.py dùng backend/domain/engine_v2 thay thế |
| backend/tsconfig.json | READY FOR DELETE | Chỉ phục vụ backend/src/**/*; backend/src/relations không còn được Production sử dụng |
| frontend-vite/src | KEEP | Không phát hiện file nghi vấn theo nhóm old/backup/test/temp/debug/legacy/orphan |
| backend/db/functions/get_family_path.sql | KEEP | SQL function có tên nghiệp vụ; chưa có dấu hiệu backup/legacy |
| backend/sql_backup/fix_old_precision.sql | VERIFY | Nằm trong sql_backup; cần xác minh còn dùng không |
| backend/sql_backup/trigger_auto_precision.sql | VERIFY | Nằm trong sql_backup; cần xác minh còn dùng không |
| backend/run_patch.bat | READY FOR DELETE | Tham chiếu patch_production_idempotent.sql không còn tồn tại; script không thể chạy |
| backup_familytreedb.sql | VERIFY | File backup DB ở root; cần xác nhận có còn cần giữ sau khi Railway DB đã import |
| _archive_tests/backend_tests_debug/debug_relationship_path_vi.py | READY FOR DELETE | Nằm trong archive test/debug; không thuộc Production |
| backend/sql_backup/fix_old_precision.sql | KEEP | Migration script chạy một lần để chuẩn hóa dữ liệu; nên lưu làm lịch sử kỹ thuật |
| backend/sql_backup/trigger_auto_precision.sql | KEEP | Migration/trigger script cho MySQL; là tài liệu kỹ thuật triển khai, không phải tàn dư |
| backend/_orphan_ARCHIVE | READY FOR DELETE | Không phát hiện import, router hoặc tham chiếu từ Production; chỉ chứa mã archive/orphan
| backend/routers/marriage_router.py | READY FOR DELETE | Không còn được import; production dùng backend/api/marriage.py
## Thu gọn lại kết 
File	Status	Evidence
backend/api/clean_parent_api_old.py	READY FOR DELETE	Không import; không router; không frontend gọi
backend/app.py	READY FOR DELETE	Flask legacy; Production dùng backend/main.py; hardcode DB localhost
backend/run_patch.bat	READY FOR DELETE	Tham chiếu patch_production_idempotent.sql không còn tồn tại; script không thể chạy
backend/tsconfig.json	READY FOR DELETE	Chỉ phục vụ backend/src/**/*; backend/src/relations không còn được Production sử dụng
backend/src/relations/*	READY FOR DELETE	Backend/Frontend không tham chiếu trực tiếp; relationship.py dùng backend/domain/engine_v2
_archive_tests/backend_tests_debug/debug_relationship_path_vi.py	READY FOR DELETE	Archive test/debug; không thuộc Production
backup_familytreedb.sql	KEEP (Archive)	Backup DB cũ; không phải bản dump Railway mới nhất
backend/api/gene_propagate.py	KEEP	backend/services/parent_child_service.py đang import
backend/db_helper.py	KEEP	backend/api/person.py đang sử dụng
frontend-vite/src	KEEP	Không phát hiện file nghi vấn theo tiêu chí cleanup
backend/db/functions/get_family_path.sql	KEEP	SQL function nghiệp vụ
backend/sql_backup/fix_old_precision.sql	KEEP	Migration script chuẩn hóa dữ liệu; lưu lịch sử kỹ thuật
backend/sql_backup/trigger_auto_precision.sql	KEEP	Migration/trigger script; lưu lịch sử triển khai