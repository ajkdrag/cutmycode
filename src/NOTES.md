`data/`: We can pull data from db, extern api, filesystem etc within it, but it must conform to some repository pattern.
`interfaces/`: We can have multiple interfaces, web, cli, api etc. Each interface has its own views, templates, static files etc.
`domain/`: We can have multiple entities, user, post, comment etc. Our business logic will deal with entities. Also contains repository interfaces (that are implemented by data providers in `data/` such as db/ etc ).
`usecases/`: We can have multiple usecases, create_user, create_post, create_comment etc. Each usecase will deal with one or more entities, categorize them by bounded context.
