import os

class Iteration(dict):
    """
    Parses output generated by an iteration of gatling testing
    """

    success_percentage_ok_tag = 'Global percentage of requests OK is equal to'
    mean_response_time_ok_tag = 'Global : mean response time is less than'
    mean_response_time_tag = "> meanResponseTime"
    report_location_tag = 'Please open the following file'

    success_percentage_ok = 'success_percentage_ok'
    mean_response_time_ok = 'mean_response_time_ok'
    mean_response_time = 'mean_response_time'
    report_location = 'report_location'

    def __init__(self, users, duration, webheads, output):
        """
        Initializes to default dict and then parses output

        :param output: StringIO buffer to read from
        """
        self.update({
            'users': users,
            'duration': duration,
            'webheads': webheads,
            self.success_percentage_ok: False,
            self.mean_response_time_ok: False,
            self.mean_response_time: None,
            self.report_location: None
        })
        self._parse(output)

    def _parse(self, output):
        """
        Parses the StringIO buffer output.  Results are stored
        over what is already saved.

        :param output: StringIO Buffer to parse from
        """
        for line in output:
            if line.startswith(self.success_percentage_ok_tag):
                if line[-5:-1] == 'true':
                    self[self.success_percentage_ok] = True
            elif line.startswith(self.mean_response_time_ok_tag):
                if line[-5:-1] == 'true':
                    self[self.mean_response_time_ok] = True
            elif line.startswith(self.mean_response_time_tag):
                self[self.mean_response_time] = line.split()[2]
            elif line.startswith(self.report_location_tag):
                self[self.report_location] = line.split()[-1]

    @property
    def success(self):
        return self[self.success_percentage_ok] and \
            self[self.mean_response_time_ok]

    @property
    def report(self):
        return self[self.report_location]

    @property
    def simulation_log(self):
        return os.path.join(os.path.dirname(self.report), 'simulation.log')

    @property
    def webheads(self):
        return self['webheads']

    @property
    def users(self):
        return self['users'] * len(self.webheads)

    @property
    def duration(self):
        return self['duration']

    def __str__(self):
        return "\n\t".join([
            "Gatling Iteration of %s users over %s seconds" % (self.users, self.duration),
            "Webheads: %s" % self.webheads,
            "Successful: %s" % self.success,
            "Successful request percentage pass: %s" % self[self.success_percentage_ok],
            "Mean response time pass: %s" % self[self.mean_response_time_ok],
            "Mean response time: %s ms" % self[self.mean_response_time],
            "Report location: %s" % self.report,
            "Simulation log: %s" % self.simulation_log])
            
