from xml.sax import saxutils


class TestReport:
    settings = None

    @staticmethod
    def group_result(result):
        rmap = {}
        classes = []
        for case in result:
            cls = case.__class__
            if cls not in rmap:
                rmap[cls] = []
                classes.append(cls)
            rmap[cls].append(case)
        r = [(cls, rmap[cls]) for cls in classes]
        return r

    @staticmethod
    def get_attributes(result, start_time, stop_time, settings):
        start_datetime = str(start_time)[:19]
        stop_datetime = str(stop_time)[:19]
        duration = (stop_time - start_time).total_seconds()

        passed, failed, error, skipped = 0, 0, 0, 0

        if result.success_count:
            passed = result.success_count
        if result.fail_count:
            failed = result.fail_count
        if result.error_count:
            error = result.error_count
        if result.skip_count > 0:
            skipped = result.skip_count

        total = passed + failed + error + skipped

        success_rate = str((passed * 100) / total) + "%"

        return dict(start_time=start_datetime, stop_time=stop_datetime, duration=duration, success=passed, fail=failed,
                    error=error, skip=skipped, total=total, success_rate=success_rate,
                    project_name=settings.PROJECT_NAME,
                    application_name=settings.APPLICATION_NAME, app_version=settings.APP_VERSION,
                    platform=settings.PLATFORM)

    @staticmethod
    def get_test_report(result):
        test_cases = []
        success, failed, error, skipped = 0, 0, 0, 0
        for tid, case in enumerate(result):
            tid = tid + 1
            name = case.id().split('.')[-1]
            doc = case.shortDescription() or ""
            desc = doc and ('%s: %s' % (name, doc)) or name

            executed = True
            if case.result == "success":
                success += 1
            elif case.result == "fail":
                failed += 1
            elif case.result == "error":
                error += 1
            elif case.result == "skip":
                skipped += 1
                executed = False

            if isinstance(case.output, str):
                uo = case.output
            else:
                uo = case.output.decode('latin-1') if case.output else ""

            if isinstance(case.traceback, str):
                ue = case.traceback
            else:
                ue = case.traceback.decode('latin-1') if case.traceback else ""

            if isinstance(case.reason, str):
                usk = case.reason
            else:
                usk = case.reason.decode('latin-1') if case.reason else ""

            case_result = dict(
                case_id=tid,
                result=case.result,
                desc=desc,
                executed=executed,
                stack_trace=saxutils.escape(ue).replace('''"''', ''),
                output=saxutils.escape(uo).replace('''"''', ''),
                skip_reason=saxutils.escape(usk).replace('''"''', '')
            )
            test_cases.append(case_result)
        overall_result = error > 0 and 'error' or failed > 0 and 'fail' or 'success'
        group = dict(
            result=overall_result,
            total=success + error + failed + skipped,
            success=success,
            error=error,
            failed=failed,
            skipped=skipped,
            test_cases=test_cases
        )
        return group

    @classmethod
    def get_suite_report(cls, result):
        groups = []
        group_result = cls.group_result(result.result)
        for cid, (kls, kls_results) in enumerate(group_result):

            if kls.__module__ == "__main__":
                name = kls.__name__
            else:
                name = "%s.%s" % (kls.__module__, kls.__name__)
            doc = kls.__doc__ and kls.__doc__.split("\n")[0] or ""
            desc = doc and '%s: %s' % (name, doc) or name

            group = dict(
                group_id=cid + 1,
                desc=desc
            )
            group.update(
                cls.get_test_report(kls_results)
            )
            groups.append(group)
        return groups

    @classmethod
    def generate(cls, result, start_time, stop_time):
        attributes = cls.get_attributes(result, start_time, stop_time, cls.settings)
        report = cls.get_suite_report(result)
        return dict(
            report=report,
            report_attributes=attributes,
        )
