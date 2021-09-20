def paperTag():
    global paperTags
    paperTags = []
    paperTags.append("@identifier")
    paperTags.append("@doi1")
    paperTags.append("@studies")
    paperTags.append("@doi2")
    paperTags.append("@date")

def doiTag():
    global doiTags
    doiTags = []
    doiTags.append("@identifier")
    doiTags.append("@dioInformation")
    doiTags.append("@doi2")
    doiTags.append("@date")

def relationTag():
    global relationTags
    relationTags = []
    relationTags.append("@identifier")
    relationTags.append("@statement1")
    relationTags.append("@relation")
    relationTags.append("@statement2")
    relationTags.append("@date")

def studyTag():
    global studyTags
    studyTags = []
    studyTags.append("@identifier")
    studyTags.append("@otherclasses")
    studyTags.append("@firstAuthorOrigin")
    studyTags.append("@doi")
    studyTags.append("@date")

def reviewTag():
    global reviewTags
    reviewTags = []
    reviewTags.append("@identifier")
    reviewTags.append("@doi1")
    reviewTags.append("@reviewInformation")
    reviewTags.append("@doi2")
    reviewTags.append("@date")
