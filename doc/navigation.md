# Navigation

Die Navigation stellt im Projekt offensichtlich eine Schwierigkeit dar. Die Navigation wird nötig, wenn wir anfangen über eine Webapp mit seperatem Backend nachzudenken. Ich werde hier Ideen sammeln, wie die Navigation funktionieren könnte und werde versuchen so viele Cases wie möglich zu überdenken bevor ich mit der Implementierung beginne. Ich habe in textual requirements beschrieben, dass ich mir pro AssetType zwei Seiten vorstelle. Damit meine ich eine Seite bei der eine Art "Listen Ansicht" verfügbar ist, es stehen alle Elemente des AssetTypes zur Verfügung (Wie der Nutzer diese Daten dann darstellt ist den Plugins überlassen). Die zweite Seite ist eine Detailansichtsseite für ein Asset. Diese Seite gehört dann aber eigentlich nicht mehr zum AssetType, sondern zum Asset.

Bei der Navigation sollte berücksichtigt werden, dass Routen zur Verfügung stehen, mit denen die Manager Funktionen direkt zur Verfügung stehen. So können speziell angepasste Frontends auf dem Framework entwickelt werden und nachträglich auf die bestehende Software aufgesetzt werden. 

## AssetType Übersicht ``/{asset_type.asset_name}/``
Eine Übersichtsseite für einen AssetType. Hier stehen alle Assets mit besagtem AssetType zur Verfügung. Diese Seite muss mit Plugins vom User ausgestaltet werden.

## Asset Detail Ansicht ``/{asset_type.asset_name}/{asset_id}