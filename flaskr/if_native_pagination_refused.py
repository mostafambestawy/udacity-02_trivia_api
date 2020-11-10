QUESTIONS_PER_PAGE = 10
def paginate(request,selection):
    page=request.args.get('page',1,type=int)
    start=(page-1)*QUESTIONS_PER_PAGE
    end=start+QUESTIONS_PER_PAGE
    return [q.format() for q in selection][[start:end]