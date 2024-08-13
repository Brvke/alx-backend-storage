#!/usr/bin/env python3
""" module for the top_student function """


def top_students(mongo_collection):
    """
        Args:
            mongo_collection: a pymongo collection object
        Returns:
            a list of dicts orderd by a studnets average score
    """

    # query for all documents in the students collection
    studnet_list = mongo_collection.find({})

    # turn the returnes Cursor object into a list of dicts
    students = [studnet for studnet in studnet_list]
    return_list = []

    # loop over the list
    for student in students:
        # empty dict to hold new dict with averageScore key
        return_dict = {}
        # loop over the dict
        for key, value in student.items():
            # int value for calculation average values
            count = 0
            total_score = 0

            # add all keys that are not the topics key to the new dict
            if key != 'topics':
                return_dict[key] = value

            # check if no topics are registed to avoid ZeroDivison error
            if len(student['topics']) != 0:
                # loop over the list of courses and aggregate the scores
                for classes in student['topics']:
                    total_score += classes['score']
                    count += 1
            else:
                # if no scores put 0 average
                return_dict['averageScore'] = 0

            # insert new key averageScore with avergae value
            return_dict['averageScore'] = total_score / count

        # append dict with student name and average score to list of student
        return_list.append(return_dict)

    # sort by averageSScore
    sorted_lst = sorted(return_list,
                        key=lambda d: d["averageScore"],
                        reverse=True)
    return sorted_lst
