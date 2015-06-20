-- Update the database, renaming "app" to "gl_site"

UPDATE django_content_type SET app_label='gl_site' WHERE app_label='app';
UPDATE django_migrations SET app='gl_site' WHERE app='app';

ALTER TABLE app_answer RENAME TO gl_site_answer;
ALTER TABLE app_leaduserinfo RENAME TO gl_site_leaduserinfo;
ALTER TABLE app_metric RENAME TO gl_site_metric;
ALTER TABLE app_submission RENAME TO gl_site_submission;
