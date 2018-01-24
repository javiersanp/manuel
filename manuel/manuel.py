# -*- coding: UTF-8 -*-

from __future__ import absolute_import
import psycopg2
from configobj import ConfigObj

from tqdm import tqdm
from jinja2 import Template
import os
import sys


def create_index(url_config, debug=False):
    """
    Creates the index for the queries

    :param url_config: Config file
    :param debug: Enables debug mode
    :type debug: bool
    :return: None
        """

    config = ConfigObj(url_config)
    conn = psycopg2.connect(**config['report']['connection'])
    cur = conn.cursor()
    if debug:
        ex_sql = cur.mogrify(config['report']['general']['indexs'])
        print(ex_sql)
    cur.execute(config['report']['general']['indexs'])
    conn.commit()


def generate_report(url_config, debug=False):
    """
    Method to generate the report

    :param url_config: URL to the config file
    :param debug: Enables debug mode
    :type debug: bool
    :return: None
    """

    print('\n')

    config = ConfigObj(url_config)
    base_dir = os.path.join(os.getcwd(), os.path.dirname(url_config))

    conn = psycopg2.connect(**config['report']['connection'])
    cur = conn.cursor()
    if debug:
        ex_sql = cur.mogrify(config['report']['general']['subarea_sql'], config['report']['general'])
        print(ex_sql)
    cur.execute(config['report']['general']['subarea_sql'], config['report']['general'])
    data = cur.fetchall()

    result = []

    for index, poblacio in tqdm(enumerate(data), total=len(data)):
        element_vars = {}
        for element in config['report']['elements'].keys():
            sql = config['report']['elements'][element]['sql']
            if debug:
                ex_sql = cur.mogrify(sql, (str(poblacio[0]),))
                print(ex_sql)
            cur.execute(sql, (str(poblacio[0]),))
            element_vars[element] = cur.fetchall()[0]

        element_vars['id'] = int(abs(poblacio[0]))
        element_vars['name'] = poblacio[1]
        result.append(element_vars)

    conn.close()

    if not isinstance(config['report']['templates'], list):
        templates = [config['report']['templates']]
    else:
        templates = config['report']['templates']
    for template in templates:
        url_template = os.path.join(base_dir, template)
        f = open(url_template)
        base, extension = os.path.splitext(url_template)
        temp = f.read()
        f.close()
        t = Template(temp)

        report_data = t.render(data=result)
        url_out = os.path.join(base_dir, 'report'+str(extension))
        f = open(url_out, 'w')
        f.write(report_data)
        f.close()
    print ('\nDone\n')


if __name__ == "__main__":
    generate_report(sys.argv[1])
