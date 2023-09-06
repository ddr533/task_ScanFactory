import re
import sqlite3


def generate_regex(domains: list) -> str:
    """
    Генерирует регулярное выражение,
    соответствующее списку переданных доменов.
    """
    escaped_domains = [re.escape(domain) for domain in domains]
    regex_pattern = '|'.join(escaped_domains)
    return regex_pattern


def update_rules_for_domains() -> None:
    """
    Считывает доменные имена для каждого проекта из таблицы domains,
    получает регулярное выражение для доменных имен и записывает
    их в таблицу rules.
    """
    with sqlite3.connect('domains.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT project_id FROM domains')
        project_ids = cursor.fetchall()

        for project_id in project_ids:
            cursor.execute('SELECT name FROM domains WHERE project_id = ?',
                           (project_id[0],))
            names = [domain[0] for domain in cursor.fetchall()]
            regex_pattern = generate_regex(names)

            cursor.execute('SELECT * FROM rules WHERE project_id = ?',
                           (project_id[0],))
            existing_rule = cursor.fetchone()

            if existing_rule:
                cursor.execute(
                    'UPDATE rules SET "regexp" = ? WHERE project_id = ?',
                    (regex_pattern, project_id[0]))
            else:
                cursor.execute('INSERT INTO rules ("regexp", project_id)'
                               ' VALUES (?, ?)', (regex_pattern, project_id[0]))


if __name__ == '__main__':
    update_rules_for_domains()
