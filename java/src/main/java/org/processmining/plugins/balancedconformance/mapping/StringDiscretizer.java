package org.processmining.plugins.balancedconformance.mapping;

import java.util.Set;

public interface StringDiscretizer {

	public static final String ANY_VALUE = "ANY VALUE";
	public static final String SMALLER_THAN_ANY_VALUE = "&lt; ANY VALUE";
	public static final String LARGER_THAN_ANY_VALUE = "&gt; ANY VALUE";
	
	int convertToInt(String val);
	String convertToString(int val);
	
	int getUpperBound();
	int getLowerBound();
	
	Set<String> getStoredStrings();
}
