tags: python, mobiledevelopment, python3

**Why is Python unsuitable as a mobile application development language?**

**tl;dr**  
PSF made migrating to Python 3 as priority to the community, which slowed down pythonic innovations during 2006-2016, which was the defining moment in history of modern Web technologies & Mobile Technologies.

**The Root Cause: The Launch of Python 3**  
Python 3 was launched in 2008 and it didn't take off as quick as PSF expected. In order to overcome the gravity of Python 2.7 they had to deliberately kill Python 2 using numerous strategies, the main strategy is stop adding new features to Python 2.7 (a.k.a simply abandoning the world’s most popular dynamically typed language of that time).

On the contrast there were various communities that kept back-porting new Python 3 features to Python 2.7 which further slowed down Python 3 adaption. So they have to press the kill switch by declaring as Python 2.7 as legacy despite the consequences, you have to remember Python 2 was having the most modern feature set of that time compared to C, C++, Perl, Java etc. There was nothing legacy about it.

**The Nightmare of the 10-Year Transition Period (Roughly 2008–2018, with Full EOL in 2020)**  
Those 10 years transition period was a great nightmare at the worst, communities(esp library owners) were forced to keep their code compatible with both 2 & 3, which caused the testing cost to sky-rocket, this impacted developers' freedom of thinking, free flow of ideas etc. What once was a simple and elegant language suddenly became a liability because you were ‘expected’ to write in both Python 2 & 3. Productivity was the original thing that made Python popular which wasn’t the experience during the transition.

**The Emergence of "Python X"**  
In the whole 10 years Pytonists were neither coding in Python 2 nor in Python 3 there were coding an in between language(Python X) filled with hodgepodge hacks here and there without clear documentation, there were enough official guidelines for porting to Python 3 but not for maintaining the code in Python 2 & 3 since they genuinely didn’t expect such a problem would arise.

**Challenges for Library Maintainers vs End Users**  
Porting from 2 -> 3 was easy for an end user, but as a library owner maintaining for 2 & 3 was a nightmare. Many libraries were simply abandoned.

**Impact on Learning and Resources**  
Learning experience of Python via internet met the all time low, Googling questions would lead to blog posts and Stackoverflow which had snippets for Python 2. Every archived knowledge (even as simple as ‘sorting a dict’) had to be re-written once again for Python 3 and tagged with proper Python versions. This part caused great confusion for newbies and made JavaScript as a possible first language. Most of the Stack overflow answers stopped working suddenly since they were originally written for Python 2. New answers were not written as often asking same question for Python 3 will cause the question to be down-voted, locked & deleted or marked as duplicate by less informed random moderators who weren’t aware of this Python specific issue, also Stackoverflow was not designed to converse around questions of multiple versions of a same programming language.

**Decline of GUI and Cross-Platform Tools**  
Great tools like WxPython, PyQT, PySide became old & oblivious because 'Python 3' was suddenly imposed as priority. (Imagine you as a open source developer, suddenly PSF/community declares your work as deprecated, you might lose the spirit, you wouldn’t care much, that’s what happened to 100s of libraries, great libraries were declared legacy even thought they were working fine, just because PSF wanted to push Python3. It wasn’t indeed to kill 100s libraries just because the author didn’t have time/interest in porting(a.k.a maintaining in 2&3)

**The Hidden Cost for Library Owners**  
The experience of porting to Python 3 was not as easy as you imagine or the PSF thought. For a developer it may be simply moving to 2 to 3. But for a library owner it is all about ‘maintaining’ 2 and 3 at the same time, with added testing cost.

**Lack of Innovation During a Critical Decade**  
Thus, everyone witnessed that during 2006 to 2016 there were no innovation or ground breaking things happened in Python's world, they were busy in solving Python 3 transition (porting & maintaining) and releasing small features by barely keeping the heads on the water. However we all knew 2006-2016 was the defining moment of web technology and mobile technologies.

JavaScript started dominating everywhere with revolutionary frameworks and new ways of doing things(like non-blocking IO, web sockets etc) while Python community were busting their head around in cleaning the mess. Python 3 is good but wrongly timed. This is why Python doesn't have a suitable cross platform framework for mobile.

While C# has Xamarin, JS has Cordova & Titanium, even Lua has Corona, but Python equivalents Kivy and PyQT do keep stalling.

**Python's Strengths in Other Domains**  
However, Python will have a strong future on the machine learning, NLP, statistical and scientific computing. So to repeat the point Python lost whatever it deserved from 2006–2016, but it will dominate what it really deserves from 2016–2026, unfortunately mobile development(front-end) isn’t one of them.