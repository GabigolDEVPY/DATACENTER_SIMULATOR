<!DOCTYPE html>

<html xmlns:h="http://xmlns.jcp.org/jsf/html">

<h:head>

<title>Excluir Livro</title>

</h:head>

<h:body>

<h2>Excluir Livro</h2>

<h:form>

ISBN

<h:inputText value="#{livroBean.isbn}" />

<h:commandButton value="Excluir"
action="#{livroBean.excluir}" />

</h:form>

</h:body>

</html>