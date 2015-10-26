library(class)
library(e1071)
library(rpart)
library(MASS)
options(warn=-1)
decision_tree_classifier <- function(train, test, class){
	formula <- as.formula(paste(class," ~ ."))	
	decision_tree<-rpart(formula, data=train, parms=list(split='information'), minsplit=2, method='class')
	decision_tree_array<-as.numeric(predict(decision_tree,newdata=test,type="vector"))
	test_data_arr<-as.numeric(test[[class]])
	acc<-length(which(decision_tree_array==test_data_arr))/length(test_data_arr)
	return(acc*100)
}
svm_classifier <- function(train, test, class){
  formula <- as.formula(paste(class," ~ ."))
  svp <- svm(formula, data=train, kernel="linear")
  pred <- predict(svp,test)
  accuracy<-(sum(diag(table(pred, test[[class]])))/sum(table(pred, test[[class]])))*100
  return(accuracy)
}

naive_bayes_classifier <- function(train, test, class){
	formula <- as.formula(paste(class," ~ ."))
  naive_bayes_model <- naiveBayes(formula, data = train)
  pred<-predict(naive_bayes_model, test)
  accuracy<-(sum(diag(table(pred, test[[class]])))/sum(table(pred, test[[class]])))*100
}

knn_classifier <- function(train, test, class){
	        k <- 5
	        Class <- train[[class]]
		actual <- test[[class]]
	        train[[class]] <- NULL
	        test[[class]] <- NULL	        
	        train[,-1] <- as.double(gsub("%", "", as.matrix(train[,-1])))
	        test[,-1] <- as.double(gsub("%", "", as.matrix(test[,-1])))	
	        train[is.na(train)] <- 0.0  
	        test[is.na(test)] <- 0.0  	             
		predicted <- knn(train, test, Class, k, l = 0, prob = FALSE, use.all = TRUE)
		count=0
		a <- 1:length(actual)
		for(q in a){
			if(actual[q]==predicted[q]){
				count = count+1
			}
		}
		return(count/length(actual)*100)
}

args <- commandArgs(TRUE)
dataURL<-as.character(args[1])
header<-as.logical(args[2])
d<-read.csv(dataURL,header = FALSE)
# create 10 samples
set.seed(123)

svm_acc <- c()
naive_bayes_acc <- c()
knn_acc <- c()
decision_tree_acc <- c()

for(i in 1:10) {
  cat("Running sample ",i,"\n")
  sampleInstances<-sample(1:nrow(d),size = 0.9*nrow(d))
  trainingData<-d[sampleInstances,]
  testData<-d[-sampleInstances,]
 
  Class<-as.factor(as.integer(args[3]))
  class <- paste("V", Class,sep="")
  
  decision_tree_acc <- c(decision_tree_acc, decision_tree_classifier(trainingData, testData, class))
  svm_acc <- c(svm_acc, svm_classifier(trainingData, testData, class))
  naive_bayes_acc <- c(naive_bayes_acc,  naive_bayes_classifier(trainingData, testData, class))
  knn_acc <- c(knn_acc,  knn_classifier(trainingData, testData, class))
  
}

print(paste("Decision Tree: ", sum(decision_tree_acc)/length(decision_tree_acc)))
print(paste("SVM: ", sum(svm_acc)/length(svm_acc)))
print(paste("Naive: ", sum(naive_bayes_acc)/length(naive_bayes_acc)))
print(paste("KNN: ", sum(knn_acc)/length(knn_acc)))
options(warn=0)
