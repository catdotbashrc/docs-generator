# Pure Maintenance MVP - 2-Week Sprint Workflow

## Mission Statement
**"Day One Impact"** - Build a demonstrable daily maintenance extractor that saves 7+ minutes every morning for ops teams.

## Success Criteria
✅ **Week 1 Exit**: Working extractor generating runbooks from real Ansible code  
✅ **Week 2 Exit**: Pilot team saves 70% time on morning maintenance with our runbook  
✅ **Final Demo**: Leadership sees ROI and approves broader rollout  

---

## WEEK 1: Build Core Extractor (Velocity Focus)

### Day 1-2: Monday-Tuesday (Setup & Simplify)
**Owner**: Backend Developer  
**Deliverable**: Simplified daily-only extractor  

```python
# Morning (4 hours)
□ Strip temporal_maintenance_extractor.py to ONLY daily patterns
□ Remove weekly/monthly/quarterly/annual logic
□ Focus on 5 key patterns:
  - Service status checks
  - Log rotation/review
  - Permission validation
  - Health checks
  - Connectivity tests

# Afternoon (4 hours)
□ Create test suite with 10 real Ansible modules
□ Verify extraction of daily patterns
□ Document found patterns in extraction_patterns.md
```

### Day 3: Wednesday (Pattern Refinement)
**Owner**: Backend Developer + DevOps  
**Deliverable**: Validated extraction patterns  

```python
# Morning (4 hours)
□ Review extracted patterns with ops team
□ Identify missing daily tasks
□ Add patterns for:
  - Certificate expiry checks (if <30 days)
  - Disk space monitoring
  - Queue/backlog checks

# Afternoon (4 hours)
□ Update extractor with ops feedback
□ Re-run on test modules
□ Achieve 80% daily task capture rate
```

### Day 4: Thursday (Runbook Generator)
**Owner**: Backend Developer  
**Deliverable**: Working markdown generator  

```python
# Morning (4 hours)
□ Create RunbookGenerator class
□ Generate markdown with:
  - Checkboxes for each task
  - Time estimates (hardcoded initially)
  - Simple grouping (checks, logs, validations)

# Afternoon (4 hours)
□ Add metadata section:
  - Generated timestamp
  - Source module name
  - Total estimated time
  - Escalation contact
```

### Day 5: Friday (Integration & CLI)
**Owner**: Backend Developer + Frontend  
**Deliverable**: Working CLI command  

```bash
# Morning (4 hours)
□ Create CLI command: ddd generate-daily [ansible-file]
□ Wire extractor → generator → file output
□ Add basic error handling

# Afternoon (4 hours)
□ Test with 10 different Ansible modules
□ Generate 10 sample runbooks
□ Package for pilot team testing
```

**Week 1 Success Gate**: Can generate daily_maintenance.md from any Ansible module ✓

---

## WEEK 2: Pilot Test & Demo Prep (Potency Focus)

### Day 6-7: Monday-Tuesday (Pilot Team Test)
**Owner**: DevOps + Product Manager  
**Deliverable**: Real team using real runbook  

```bash
# Monday Morning (4 hours)
□ Identify pilot team (most daily-task heavy)
□ Record current morning routine (video)
□ Measure baseline time (expect ~10 minutes)
□ Document pain points

# Monday Afternoon (4 hours)
□ Generate runbook from their actual playbooks
□ Review with team lead
□ Adjust format based on feedback
□ Finalize for Tuesday test

# Tuesday Morning (4 hours)
□ Team executes morning tasks using runbook
□ Record new routine (video)
□ Measure new time (target: 3 minutes)
□ Capture team feedback

# Tuesday Afternoon (4 hours)
□ Calculate time savings
□ Document what worked/didn't work
□ Get testimonial quotes
□ Prepare metrics summary
```

### Day 8: Wednesday (Demo Assets)
**Owner**: Product Manager + Designer  
**Deliverable**: Demo presentation materials  

```bash
# Morning (4 hours)
□ Create 5-slide deck:
  1. Problem: "10 minutes every morning"
  2. Solution: "Automated extraction"
  3. Demo: "Live runbook generation"
  4. Results: "70% time reduction"
  5. Scale: "Every team, every day"

# Afternoon (4 hours)
□ Edit before/after videos (30 sec each)
□ Create ROI calculator spreadsheet
□ Prepare live demo script
□ Practice demo flow (3 minutes max)
```

### Day 9: Thursday (Polish & Iterate)
**Owner**: Full Team  
**Deliverable**: Production-ready demo  

```bash
# Morning (4 hours)
□ Dry run with internal stakeholders
□ Incorporate feedback
□ Fix any extractor bugs found
□ Optimize runbook format

# Afternoon (4 hours)
□ Final demo rehearsal
□ Prepare backup plan (pre-generated runbooks)
□ Test all equipment/screens
□ Final slide polish
```

### Day 10: Friday (Leadership Demo)
**Owner**: Product Lead  
**Deliverable**: Executive buy-in  

```bash
# Morning (2 hours prep)
□ Final rehearsal
□ Setup demo environment
□ Pre-generate safety runbooks

# Demo Time (30 minutes)
□ 0:00-0:05 - Problem statement with metrics
□ 0:05-0:10 - Live extraction demo
□ 0:10-0:15 - Show pilot team results
□ 0:15-0:20 - ROI calculation
□ 0:20-0:25 - Rollout plan
□ 0:25-0:30 - Q&A

# Afternoon (2 hours)
□ Capture feedback
□ Document commitments
□ Plan Week 3 based on response
```

---

## Technical Implementation Details

### Simplified Daily Extractor (Week 1 Focus)
```python
class DailyMaintenanceExtractor:
    """Ultra-simple daily task extractor - MVP version."""
    
    DAILY_PATTERNS = [
        # Service checks
        (r'service.*status', 'Check {service} status', 2),
        (r'systemctl.*status', 'Verify {service} is running', 2),
        
        # Log operations
        (r'tail.*log', 'Review recent log entries', 3),
        (r'grep.*error.*log', 'Check logs for errors', 3),
        (r'logrotate', 'Verify log rotation', 1),
        
        # Health checks
        (r'ping|curl.*health', 'Test connectivity/health', 2),
        (r'df\s+-h', 'Check disk space', 1),
        
        # Validations
        (r'test\s+-[rwx]', 'Validate permissions', 2),
        (r'find.*-mtime', 'Check for stale files', 2),
    ]
    
    def extract(self, ansible_content):
        tasks = []
        for pattern, description, minutes in self.DAILY_PATTERNS:
            if re.search(pattern, ansible_content, re.IGNORECASE):
                tasks.append({
                    'description': description,
                    'time_minutes': minutes,
                    'pattern': pattern
                })
        return tasks
```

### Simple Runbook Generator (Week 1 Focus)
```python
class RunbookGenerator:
    """Dead simple markdown generator - MVP version."""
    
    def generate(self, tasks, module_name):
        total_time = sum(t['time_minutes'] for t in tasks)
        
        return f"""# Daily Maintenance Runbook
**Module**: {module_name}  
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}  
**Estimated Time**: {total_time} minutes  

## Morning Checklist

{"".join([f"- [ ] {t['description']} ({t['time_minutes']} min)\n" for t in tasks])}

## Completion
- [ ] All checks passed
- [ ] Any issues escalated
- [ ] Time recorded: _____ minutes

## Escalation
If any check fails, contact: [ON-CALL]
"""
```

---

## Risk Mitigation

### Week 1 Risks
- **Pattern matching too simple**: Have ops team review patterns Day 3
- **Missing critical daily tasks**: Get ops input before coding
- **Runbook format unusable**: Show mockup Day 2, iterate

### Week 2 Risks  
- **Pilot team unavailable**: Have backup team identified
- **No time savings achieved**: Focus on process clarity even if time same
- **Demo technical failure**: Pre-generate all runbooks as backup

---

## Success Metrics

### Week 1 Metrics
- [ ] 10+ Ansible modules processed
- [ ] 80%+ daily tasks captured  
- [ ] Runbook generated in <1 second
- [ ] CLI tool working end-to-end

### Week 2 Metrics
- [ ] Pilot team time: 10 min → 3 min (70% reduction)
- [ ] Team willing to use tomorrow: Yes/No
- [ ] Leadership approval for expansion: Yes/No
- [ ] ROI calculation validated: $$$ saved/year

---

## Post-MVP Roadmap (Weeks 3-4)

**Only After Proven Success:**

Week 3: Add weekly tasks + automation stubs  
Week 4: Add second tool (Terraform or K8s)  
Week 5-6: Enterprise features (audit trail, compliance)  
Week 7-8: Scale to 10 teams  
Week 9-12: Full temporal framework  

---

## The Core Principle

**Velocity > Potency > Breadth**

We're not building the perfect solution. We're building the fastest path to demonstrated value. Every decision should optimize for "Can we demo this Friday?"

If it doesn't help the demo, it doesn't go in the MVP.