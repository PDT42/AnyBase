# Domain Analysis

## Resource
Eine Resource ist **ein** Datensatzelement. Jede Resource hat einen ResourceType.

## RecourceManager
Der ResourceManager verwaltet die Resourcen. Er stellt das Interface zwischen der Datenbank und dem Backend dar. Über ihn könnnen Resourcen abgerufen, erstellt und verwaltet werden. 

## ResourceType
Ein ResourceType definiert die Felder einer Resource. ResourcenTypen müssen in einer eigenen Datenbank gehalten werden, die beim StartUp der Software gelesen wird. 

## ResourceTypeManager
Der ResourceTypeManager verwaltet die ResourceTypes. Er stellt das Interface zwischen der Datenbank und dem Backend dar. Über ihn können ResourcenTypen erstellt und verwaltet werden.

## User
Nutzer im System. Nutzer haben einen UserType, mit dem ihr Accesslevel angegeben wird. 

## UserType
Wird an User vergeben. Vom UserType ist das Accesslevel von Nutzern abhängig.

## Plugin
Plugins sind das Herzstück von AnyBase. Plugin ist darum ein Interface, auf Basis dessen alle anderen Plugins funktionieren. Ein Plugin braucht dementsprechend eine Datenbankanbindung, mit Hilfe derer es auf den Datenbestand des Users zugreifen kann. Ein Plugin hat außerdem ein Data Requirement, getypte Pflichtfelder, deren required Types mit den zur Verfügung gestellten verglichen werden kann. Für einen solchen Vergleich muss natürlich außerdem der ResourceType zur Verfügung stehen, mit dem das Plugin arbeitet. Es könnte notwendig werden, dass Plugins auf mehr als einen ResourceType zugreifen müssen.   

## Layout
Ein Layout ist eine bestimmte Seitenaufteilung, die der Nutzer für eine ResourcePage oder eine ResourceDetailPage festlegen kann.

## Template
Ein Template ist die Frontend Repräsentation eines Plugins.

## ResourcePage
Eine ResourcePage ist die Übersichtsseite für einen bestimmten ResourceType.

## ResourceDetailPage
Eine ResourceDetailPage ist die Übersichtsseite für eine Resource eines bestimmten ResourceTypes.