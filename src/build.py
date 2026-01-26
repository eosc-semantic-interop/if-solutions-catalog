import jinja2
from collections import defaultdict
import os 
import frontmatter

SOLUTION_SUMMARY_TEMPLATE = """---
hide: toc
---
{% for type, grouped_solutions in solutions_by.items() %}

### {{ type }}

{% for solution in grouped_solutions %}
#### [{{ solution.title }}]({{ solution.url }})

{{solution.desc}}

{% endfor %}
{% endfor %}

"""

SOLUTION_SUMMARY_TEMPLATE2 = """---
hide: toc
---
{% for type, grouped_solutions in solutions_by.items() %}

### {{ type }}

{% for solution in grouped_solutions %}
#### [{{ solution.title }}]({{ solution.url }})

{{solution.desc}}

{% endfor %}
{% endfor %}

"""

def map_pid(id):
    if id == 'S1':
        return 'S1 — Lack of common definitions'
    if id == 'S2':    
        return 'S2 — Lack of shared semantic artefacts'
    if id == 'S3':
        return 'S3 — Lack of reference repositories for semantic artefacts'
    if id == 'S4':
        return 'S4 — Poor documentation and fragmented metadata schemas'
    if id == 'S5':
        return 'S5 — Lack of semantic expertise in communities'
    if id =='T1':
        return 'T1 — Fragmented authentication and authorisation'
    if id == 'T2':
        return 'T2 — Heterogeneous data formats'
    if id == 'T3':
        return 'T3 — Difficulty finding data at different granularities'
    if id == 'T4':
        return 'T4 — PID fragmentation and inconsistency'
    else:
        return 'Unknown'

def build():
    jinja_env = jinja2.Environment()
    solution_summary_template =jinja_env.from_string(SOLUTION_SUMMARY_TEMPLATE)
    solution_summary_template2 =jinja_env.from_string(SOLUTION_SUMMARY_TEMPLATE2)

    solutions_by_type = defaultdict(list) 
    solutions_by_problem = defaultdict(list) 
    solutions_dir = 'docs/solutions/'
    for filename in sorted(os.listdir(solutions_dir)):
        if filename.endswith(".md"):
            filepath = os.path.join(solutions_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                #print(filepath)
                post = frontmatter.load(f)    

                metadata = {
                    "title": post.get("title", "Untitled"),
                    "desc": post.get("desc", "Unknown"),
                    "type": post.get("type", "Unknown"),
                    "status": post.get("status", "Unknown"),
                    'url': 'solutions/' + filename.rsplit( ".", 1 )[0] + '.md',
                    'problem_id': post.get("problem_id", []),
                    "content": post.content
                }
                
                solutions_by_type[metadata["type"]].append(metadata)
                for pid in metadata['problem_id']:
                    if pid in ['S1', 'S2', 'S3', 'S4', 'S5', 'T1', 'T2', 'T3', 'T4']:
                        metadata['problem_name'] = map_pid(pid)
                        solutions_by_problem[map_pid(pid)].append(metadata)

                    else:
                        solutions_by_problem['Unknown'].append(metadata)
                
    # Sort cases within each mapping type by title
    for type in solutions_by_type:
        solutions_by_type[type].sort(key=lambda x: x["title"].lower())                    
    for problem in solutions_by_problem:
        solutions_by_problem[problem].sort(key=lambda x: x["title"].lower())                    

    # Sort mapping types alphabetically, but put "TBD" and "Unknown" at the end
    def mapping_type_sort_key(item):
        v = item[0]
        if v in ("TBD", "Unknown"):
            return (1, v)
        return (0, v)      
    sorted_solutions_by_type = dict(sorted(solutions_by_type.items(), key=mapping_type_sort_key))  
    sorted_solutions_by_problem = dict(sorted(solutions_by_problem.items(), key=mapping_type_sort_key))  

    with open('docs/solutions_overview_by_type.md', 'w', encoding='utf-8') as out_file:
        out_file.write(solution_summary_template.render(solutions_by=sorted_solutions_by_type))
    with open('docs/solutions_overview_by_problem.md', 'w', encoding='utf-8') as out_file:
        out_file.write(solution_summary_template2.render(solutions_by=sorted_solutions_by_problem))

if __name__ == "__main__":
    build()