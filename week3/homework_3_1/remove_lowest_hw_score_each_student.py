#!/usr/env python2.7
import pymongo
import sys

if __name__ == '__main__':

    # establish a connection to the database
    connection = pymongo.MongoClient("mongodb://localhost")
    db = connection.school
    students = db.students

    # Let's get all the unique names first
    names = list((students.find({}, {'name': 1, '_id': 0})))
    names = [name['name'] for name in names]

    # Now, iterate over all names, getting all entries corresponding to each
    # name and then we can all homeworks
    for name in names:
        entry_lists = [dict(scores=entry['scores'], _id=entry['_id']) for
                       entry in list(students.find({'name': name}))]
        hw_scores = []
        for entry_list in entry_lists:
            for _entry in entry_list['scores']:
                if _entry['type'] == 'homework':
                    hw_scores.append(dict(score=_entry['score'],
                                          _id=entry_list['_id']))
        if hw_scores:
            worst_hw_score = sorted(hw_scores,
                                    key=lambda x: x['score'])[0]
            orig_doc = students.find_one({'name': name,
                                          '_id': worst_hw_score['_id']})
            substitute_doc_scores = orig_doc['scores']
            for score_doc in substitute_doc_scores:
                if score_doc == dict(score=worst_hw_score['score'],
                                     type='homework'):
                    del substitute_doc_scores[
                        substitute_doc_scores.index(score_doc)]
            result = students.update_one({'name': name,
                                          '_id': worst_hw_score['_id']},
                                         {'$set': {'scores':
                                              substitute_doc_scores}})