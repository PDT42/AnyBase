## Workflow: Create ResourceType

Der Nutzer startet die Software zum ersten Mal. Da alle weiteren Funktionen von den Resourcen abhängen, die das System verwaltet, muss der User Resourcen und deren ResourcenTypen erstellen können. Bevor der Nutzer eine Resource erstellen kann, muss es einen Typ geben, den diese Resource haben kann. Als erstes muss der Nutzer also einen Resourcentyp erstellen. (Natürlich kann der Nutzer nicht nur beim ersten Starten der Software einen ResourceTypen anlegen, aber ich denke, bei einem leeren Screen zu beginnen ist passend. Es zeigt sehr anschaulich, dass ohne Resourcen keine weitere Interaktion sinnvoll ist.)

1. Der Nutzer pressed einen Button im Interface "Neuen Resourcentyp erstellen" (oä.).  

_Damit dieser Schritt funtkioniert, brauchen wir eine Route (im Sinne von Flask Route) zu einem Eingabefenster/Eingabepopup. Dei benötigte Funktionalität ist (ies) rein Frontend._

2. Der Nutzer beginnt mit der Eingabe der für die Definition eines Resourcentyps benötigten Werte. Jeder Resourcentyp braucht (aus der Nutzereingabe) einen ``name`` sowie die Datenfelder die die Resourcen des Resourcentyps enthalten sollen. 

_Ich stelle mir hier ein recht schlichtes Interface vor. Eine Name Box und darunter eine Liste von Values, die man mit den Resourcen des ResourceTypes assoziieren möchte. Nach der Eingabe eines Values soll die Eingabe eines Nächsten möglich sein. Keine Values anzugeben soll nicht erlaubt sein. Jeder Value braucht eine Information über den Namen des Values, sowie den Datentyp und ob der Wert ``required`` ist._

3. Der Nutzer bestätigt die Erstellung und bekommt Feedback über Erfolg oder Fehlschlag der Operation.

_Beim Anlegen eines Resourcentyps wird eine ``resouce_type_id`` vergeben, sowie der ``resource_table_name`` aus dem ``name`` des ResourceTypes generiert. Ich gehe davon aus, dass wir den erstellten ResourceType speichern müssen, bin mir da aber nicht 100% sicher. Meine initiale Idee ist, die ResourceTypes in einer eigenen internen Tabelle der Datenbank zu speichern. Die Felder einer solchen Tabelle wären dann: ``resource_type_id``, ``resource_name``, ``resource_table_name``, ``resource_columns``. Resource Columns würde folgendermaßen strukturiert sein ``"{value_name} {value_type} {int(is_resquired)} {int(is_primary_key)} ..."``. Beim erstellen von ResourceTypes sollte sichergestellt werden, dass keine zwei ResourcenTypen mit dem gleichen ``name`` erstellt werden können. Das würde zweifellos zu Verwirrung bei der Bedienung führen. Außerdem muss natürlich eine Tabelle für Resourcen dieses ResourcenTypes in der Datenbank angelegt werden._