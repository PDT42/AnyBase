# Navigation

Die Navigation stellt im Projekt offensichtlich eine Schwierigkeit dar. Die Navigation wird nötig, wenn wir anfangen über eine Webapp mit seperatem Backend nachzudenken. Ich werde hier Ideen sammeln, wie die Navigation funktionieren könnte und werde versuchen so viele Cases wie möglich zu überdenken bevor ich mit der Implementierung beginne. Ich habe in textual requirements beschrieben, dass ich mir pro ResourcenTyp zwei Seiten vorstelle. Damit meine ich eine Seite bei der eine Art "Listen Ansicht" verfügbar ist, es stehen alle Elemente des ResourcenTyps zur Verfügung (Wie der Nutzer diese Daten dann darstellt ist den Plugins überlassen). Die zweite Seite ist eine Detailansichtsseite für eine Resource. Diese Seite gehört dann aber eigentlich nicht mehr zum ResourcenTyp, sondern zur Resource.

## ResourcenTyp Übersicht ``/{resource_type.resource_name}/``
Eine Übersichtsseite für einen ResourcenTyp. Hier stehen alle Resourcen mit besagtem ResourcenTyp zur Verfügung. Diese Seite muss mit Plugins vom User ausgestaltet werden.

## Resource Detail Ansicht ``/{resource_type.resource_name}/{resource_id}