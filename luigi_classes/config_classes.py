import luigi


class VerneConfig(luigi.Config):
    username = luigi.Parameter()
    hostname = luigi.Parameter()
    remote_root = luigi.Parameter()
    target_list = luigi.Parameter()
    update_user = luigi.Parameter()
    update_token = luigi.Parameter()