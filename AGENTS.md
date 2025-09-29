# AI Agent Instructions

This document contains specific instructions for AI agents working on the EXPERIMENTAL_EmailTriageAssistant project.

## 📋 Core Responsibilities

### 🔄 Documentation Maintenance (CRITICAL)

**MANDATORY: Update documentation after EVERY action, especially commits and pushes**

#### Required Updates After Each Action:

1. **README.md** - Must be updated after:
   - ✅ Task completions (update progress sections)
   - ✅ Phase transitions (update current status)
   - ✅ Architecture changes (update tech stack/structure)
   - ✅ Test results changes (update quality assurance)
   - ✅ Before every commit/push

2. **handoff.md** - Must be updated after:
   - ✅ Completing any task or subtask
   - ✅ Changing implementation approach
   - ✅ Test results or validation status changes
   - ✅ Technical decisions or architecture updates
   - ✅ Before every commit/push
   - ✅ At end of every working session

#### Update Format:
```markdown
## Documentation Update Pattern:
1. Complete task/action
2. Update README.md current status
3. Update handoff.md with detailed state
4. Commit with clear message
5. Push changes
```

### 📝 README.md Sections to Maintain:

- **Current Status**: Always reflect latest phase and completion percentage
- **Completed**: Mark phases/tasks as ✅ when done
- **In Progress**: Update to current working area
- **Next Steps**: Update with immediate next priorities
- **Quality Assurance**: Update test counts and results

### 📝 handoff.md Sections to Maintain:

- **Date**: Update to current date
- **Current State Summary**: Reflect all recent changes
- **Validation Status**: Update test results and metrics
- **Next Phase**: Update priorities and dependencies
- **Technical Context**: Document new decisions or changes
- **Continuation Commands**: Ensure commands are current

## 🔧 Development Workflow

### Task Implementation Pattern:
1. **Start**: Read current handoff.md for context
2. **Work**: Follow TDD approach, implement systematically
3. **Validate**: Run tests, verify functionality
4. **Document**: Update README.md + handoff.md
5. **Commit**: Clear commit message with task reference
6. **Handoff**: Ensure next agent has complete context

### Git Commit Messages:
```
Format: "feat(phase): Complete T###: Description

- Specific changes made
- Test results
- Documentation updated"

Examples:
"feat(models): Complete T018-T028: Implement all 11 data models

- All Pydantic models with validation
- 12 enums for controlled vocabularies  
- 23 tests passing, 1 skipped
- README.md and handoff.md updated"
```

## 🎯 Quality Standards

### Before Every Commit:
- [ ] All tests passing (run `python -m pytest -v`)
- [ ] No syntax errors or import issues
- [ ] README.md reflects current state
- [ ] handoff.md provides complete context
- [ ] Constitutional compliance maintained

### Documentation Quality:
- **Specificity**: Include exact task numbers, test counts, file names
- **Clarity**: Next agent should understand immediately where to continue
- **Completeness**: All decisions, changes, and context documented
- **Timeliness**: Updated within same session as changes

## 🚨 Critical Rules

### NEVER:
- Skip documentation updates after completing tasks
- Commit without updating README.md and handoff.md
- Leave incomplete state undocumented
- Assume next agent has context from conversation

### ALWAYS:
- Update documentation before committing
- Include test results in documentation
- Document technical decisions and rationale
- Provide clear next steps for continuation
- Maintain project momentum through clear handoffs

## 📊 Success Metrics

A successful session includes:
- ✅ Task(s) completed according to specification
- ✅ All tests passing (or documented reasons for failures)
- ✅ README.md updated with current status
- ✅ handoff.md updated with complete state
- ✅ Changes committed with clear messages
- ✅ Next agent can continue immediately without confusion

## 🔄 Example Session Flow:

```bash
# 1. Start with context
cat handoff.md

# 2. Work on tasks
# ... implementation work ...

# 3. Validate
python -m pytest -v

# 4. Update documentation
# Edit README.md (current status)
# Edit handoff.md (detailed state)

# 5. Commit
git add .
git commit -m "feat(services): Complete T029: Storage layer with SQLCipher"

# 6. Ensure handoff ready
# Final check that handoff.md is complete
```

---

**Remember: Documentation is not optional - it's the lifeline of project continuity.**