tags: django, rest, api, drf

### “Django REST Framework: The Over-Engineered Greedy Corpse of Django Forms That Refuses to Die"

Let's start by burying REST itself real quick, because DRF is built on the rotting foundation of a 2000s architectural cargo cult that's been wheezing since [GraphQL](https://graphql.org/), [gRPC](https://grpc.io/), tRPC, and even plain JSON-RPC started laughing at it.

RESTful, the idea was great in 2006 when [Roy Fielding](https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm) was drunk on HTTP verbs and everyone pretended [HATEOAS](https://en.wikipedia.org/wiki/HATEOAS) was gonna save, decades later it's mostly a theater:  
- Over-fetching/under-fetching hell  
- N+1 query nightmares hidden behind "pagination"  
- Verb gymnastics for what should just be RPC calls  
- Versioning nightmares because you can't change anything useful without breaking clients  
- Idempotent PUT/DELETE promises that fall apart the second you touch real business logic  

REST isn't a protocol, it's a style guide nobody follows consistently. Most REST APIs are just RPC dressed in HTTP clothing with extra steps. We could roast REST for a whole post (and we should), but let's save the funeral for later. Today the victim is DRF, the greedy middle child that tried to turn Django into a REST cosplay while dragging the corpse of Django forms/templates into the API era.

### The original sin: DRF is literally Django Forms 2.0 but for JSON

Django had this beautiful (for 2005) story:  
- Models - Forms - Views - Templates  
- ModelForm auto-magics validation + rendering  
- Clean, batteries-included, beginner-friendly magic  

Then mobile/SPA/React/Vue/Flutter happened. Templates died. Forms became irrelevant for anything except admin/internal tools. The backend's job shrank to "give me JSON, validate it, save it, bye."

Instead of letting Django evolve into a clean, API-first beast, someone said:  
"Wait… what if we just slap the exact same form/model magic onto APIs? Call it Serializer instead of Form! Call it ViewSet instead of View! Reuse all the terminology so nobody has to learn anything new!"

Boom, DRF was born. Greedy as hell. It didn't innovate; it ported dying concepts to a new world and pretended it was progress.

- **ModelSerializer** = ModelForm but JSON  
- **Serializer** = Form  
- **Validation** = same clean/validate_{field} hooks  
- **to_representation** = basically render_to_response but manual  

They didn't simplify APIs. They forced every Django dev to keep thinking in form-based, server-rendered mental models when the client is now the one doing rendering/validation/display. The backend should be dumb, stateless, JSON-in/JSON-out. DRF makes it feel like you're still building a monolith MPA with extra steps.

### The boilerplate apocalypse

You want a simple CRUD for a model? In plain Django + JsonResponse:

```python
def thing_list(request):
    if request.method == 'GET':
        things = Thing.objects.all()
        return JsonResponse({'things': list(things.values())}, safe=False)
    
    if request.method == 'POST':
        data = request.data
        # parse, validate, save, return 3-20 lines max
        ...
```

20–40 lines tops for basic endpoints. Readable. Controllable. No magic.

DRF version?  
- Serializer class  
- Meta fields/exclude/depth/nested hell  
- ViewSet (or GenericAPIView + mixins)  
- Router registration  
- Override get_queryset, get_serializer_class, perform_create, etc.  
- Custom actions @action(detail=True)  
- Throttling classes, permission classes, pagination classes  

Suddenly your "simple" API requires 300+ lines across 7 files for what should be a function. Inheritance chains so deep you need a map to debug why create() is calling update() sideways. New devs stare and go "this is Python?" Nope, it's DRF cult initiation.

It's not beginner-friendly, it's Django-expert-only. New devs look at DRF code and think "this framework is fighting me." Because it is. The so called magic only works if you surrender to the DRF way. Deviate once (custom validation, non-model data, weird nesting) and you're overriding half the base classes anyway.

### Performance? What performance?
ModelSerializer is infamous for being glacially slow. Benchmarks show it 300–400× slower than plain dict conversion on simple objects. 
- ModelSerializer dynamically builds fields every request - perf hit on hot paths  
- Deep nesting + source= tricks = N+1 + slow serialization  
- High-cardinality stuff (like dynamic fields) makes caching/debugging hell  
- ViewSets encourage god-classes with 10+ methods  
- Third-party packages? Either you lock into DRF ecosystem forever or you rewrite  

Tom Christie (DRF creator) himself warned: [avoid serializers in perf-critical paths](https://hakibenita.com/django-rest-framework-slow). Yet DRF pushes them as default. In 2026, when your API hits 1k+ req/s, you're profiling and cursing because DRF decided "magic" > speed.

Meanwhile, alternatives like [Django Ninja](https://django-ninja.dev/) or plain views + [Pydantic](https://docs.pydantic.dev/)/[FastAPI](https://fastapi.tiangolo.com/)-style type hints let you write functions that look like functions. Async support? Native in Ninja/FastAPI. Auto OpenAPI? Built-in without extra config. DRF feels like it's still stuck in 2015 sync land.

### Maintenance & stagnation
Last major release? 3.14 in late 2022. Anything since 3.15 is minor fixes which are basically pushing DRF into life support.  
- No real async love, still sync-first, async hacks feel bolted-on. While Django grew async views/ORM, DRF stayed in sync land  
- Community shifting hard: Reddit/HN/Upwork points the trend of moving to FastAPI / Django Ninja for new projects  
- Django Ninja / FastAPI give auto OpenAPI, Pydantic validation, type hints, blazing perf, native async-DRF feels like a Windows XP app next to them  

Django core in 2025+ basically said "REST? Not our problem—use third-party." And people still defend DRF as "batteries-included" when it's the opposite: extra dependency that locks you out of modern Python niceties.

### More nails in the coffin
- **Ecosystem lock-in trap** - DRF plugins everywhere, but deviate once (custom auth, weird nesting, non-CRUD) and you're rewriting base classes. Good luck migrating later.  
- **Documentation overwhelm** - Official docs are a wiki maze. Click one link - 47 new concepts - infinite tabs. Beginners get lost for weeks.  
- **ViewSet god-classes** - One class handles list/create/retrieve/update/partial_update/delete + 10 custom actions. Breaks single-responsibility so hard it's comical.  
- **Pagination & throttling good? Sure** - But you can steal throttling in 50 lines. Don't need the whole framework for it.  
- **Community burnout signal** - Threads everywhere: "DRF in 2025? Why still third-party for batteries-included Django?" "Moved to Ninja—never looking back." "DRF feels bloated/clunky/stale."  

### The one good thing (because fairness)

Throttling/rate-limiting in DRF is genuinely clean. ScopedThrottler, UserRateThrottle, etc., solid. If I ever touch DRF again, it's probably just to steal the throttling middleware and throw the rest away.

But that's it. Everything else? You can roll in 20 lines of if/else + JsonResponse + basic validation. DRF is overkill for 80% of APIs and actively harmful for the rest.

### Verdict 2025: Move on
DRF was peak 2015: when REST was king and Django needed API lipstick. In 2025 it's a luxury tax on velocity, perf, and sanity. Here is how to move on:

- For simple APIs use Plain views + JsonResponse 
- For complex usecases & API docs stick to Django Ninja (FastAPI syntax + Django ORM/admin) or full FastAPI  
- For existing legacy projects, sure, maintain it. But start writing newer endpoints and versions using Django Ninja or FastAPI

Whoever starts a greenfield project with full DRF in 2025 is either trying to get paid by the line of code or hasn't profiled serialization lag yet, Or hasn't discovered they can just write functions that return JSON  

Rest in pieces, DRF. You overstayed your welcome. You were never necessary.