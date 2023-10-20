package org.qut.processmining.ab.jobs;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;

import org.deckfour.xes.in.XesXmlParser;
import org.deckfour.xes.model.XAttribute;
import org.deckfour.xes.model.XEvent;
import org.deckfour.xes.model.XLog;
import org.processmining.dataawarereplayer.precision.DataAwarePrecisionPlugin;
import org.processmining.dataawarereplayer.precision.PrecisionConfig;
import org.processmining.dataawarereplayer.precision.PrecisionResult;
import org.processmining.datapetrinets.io.DataPetriNetImporter;
import org.processmining.datapetrinets.io.DataPetriNetImporter.DPNWithLayout;
import org.processmining.models.graphbased.directed.petrinet.elements.Place;
import org.processmining.models.graphbased.directed.petrinet.elements.Transition;
import org.processmining.models.graphbased.directed.petrinetwithdata.newImpl.DataElement;
import org.processmining.plugins.balancedconformance.DataConformanceJobber;
import org.processmining.plugins.balancedconformance.config.BalancedProcessorConfiguration;
import org.processmining.plugins.balancedconformance.export.ExtendLogWithAlignments;
import org.processmining.plugins.balancedconformance.result.AlignmentCollection;
import org.processmining.plugins.balancedconformance.result.BalancedReplayResult;
import org.processmining.xesalignmentextension.XAlignmentExtension;
import org.processmining.xesalignmentextension.XAlignmentExtension.XAlignedLog;
import org.qut.processmining.ab.helpers.DataConformanceObserver;
import org.qut.processmining.ab.helpers.progressListener;

import com.google.common.collect.HashMultimap;
import com.google.common.collect.SetMultimap;

public class MannhardtPrecision {

	public static void main(HashMap<String,String> args) throws Throwable {
		FileWriter writer = null;
		try {
		// check for all required cmd args 
		if (requires(args) == false) {
			System.out.println("Cannot run job, requires the following inputs:");
			System.out.println("--log : path to original log");
			System.out.println("--model : path to dpn folder");
			System.out.println("--output: path to outpu folder");
			System.out.println("cmd args passed were: "+args.keySet());
			return;
		}
		// load in the .xes.gz log 
		XLog log = null;
		writer = new FileWriter(new File(args.get("output")+"\\scores.csv"));
		writer.write("log,model,mean,\n");
		try {
			System.out.println("[Job] parsing log...");
			log = new XesXmlParser().parse(new File(args.get("log"))).get(0);
		} catch (Exception ie) {
			System.out.println("[Job] Unable to parse log: "+args.get("log"));
			throw ie.getCause();
		}
		// load in dpn
		
		String dpnPath = args.get("model");
			// load in DPN
			DPNWithLayout dpn = null;
			System.out.println("[Job] loading dpn...");
			try {
				dpn = new DataPetriNetImporter().importFromStream(new FileInputStream(dpnPath));
			} catch (Exception ie) {
				System.out.println("[Job] error: unable to parse pnml into petrinet and on to dpn");
				throw ie;
			}
		//  find fitting log
		XLog alignedLogs = null;
		System.out.println("[Job] computing fitting log");
		try {
			System.out.println("[Job] parsing aligned log...");
			progressListener plug = new progressListener();
			DataConformanceObserver obs = new DataConformanceObserver();
			BalancedProcessorConfiguration config = BalancedProcessorConfiguration.newDefaultInstance(
					dpn.getDPN(),
					dpn.getDPN().getInitialMarking(),
					dpn.getDPN().getFinalMarkings(),
					log,
					log.getClassifiers().get(0),
					MannhardtRecall.defaultMoveOnModelCost,
					MannhardtRecall.defaultMoveOnLogCost,
					MannhardtRecall.defaultMissingWriteOpCost,
					MannhardtRecall.defaultIncorrectWriteOpCost
			);		
			config.setObserver(obs);
			// default settings update for computation limits						
			config.setTimeLimitPerTrace(MannhardtRecall.configMaxTraceCompute);
			// set default limits for variables
			BalancedProcessorConfiguration.autoGuessBounds(config, dpn.getDPN(), log);
			// adjustments for deleoni
			config.setActivateDataViewCache(false);
			config.setKeepDataFlowSearchSpace(false);
			config.setUsePartialDataAlignments(false);
			// set amount of processors to be one less 
			config.setConcurrentThreads(config.getConcurrentThreads()-1);
			System.out.println("[Job] lower: " + config.getLowerBounds().toString());
			System.out.println("[Job] upper: " + config.getUpperBounds().toString());
			// compute conformance checking						
			BalancedReplayResult result = new DataConformanceJobber().doBalancedAlignmentDataConformanceChecking(
					dpn.getDPN(),
					log,
					new progressListener(),
					config
			);
			alignedLogs = ExtendLogWithAlignments.doExtendLogWithAlignments(plug, (AlignmentCollection) result);
		} catch (Exception ie) {
			System.out.println("[Job] Unable to compute fitting log: "+args.get("alog"));
			throw ie.getCause();
		}
		// run precision test
		PrecisionResult result = run(log,alignedLogs,dpn);
		writer.write(args.get("log")+","+args.get("model")+","+result.getPrecision()+",\n");
		HandlePlaceDump(result,args,"1",dpn);
		writer.close();
		} catch (Exception e) {
			System.out.println("[Job] Error occured: "+e.getMessage());
			writer.close();
			throw e.getCause();
		}
	} 
	
	public static boolean requires(HashMap<String,String> args) {
		if (args.containsKey("model")) {
			if (args.containsKey("log")) {
					if (args.containsKey("output")) {
						return true;
					}
			}
		}
		return false;
	}
	
	public static void HandlePlaceDump(PrecisionResult results, HashMap<String,String> args, String job, DPNWithLayout dpn) throws Throwable {
		FileWriter dumper = new FileWriter(new File(args.get("output")+"place_scores.csv"));
		dumper.write("place_name,precision,occurences\n");
		//	for each place in the dpn record the place precision and the occurrences of that place in the log
		for(Place place: dpn.getDPN().getPlaces()) {
			if (place.getGraph().getOutEdges(place).size() > 1) {
				String line = "";
				line += place.getLabel()+",";
				line += results.getPrecision(place)+",";
				long frequencySum = results.getPossibleStateTransitions(place).keySet().stream().map(state -> results.getFrequency(state)).reduce((long)0, (a,b) -> a+b);
				line += frequencySum+"\n";
				dumper.write(line);
			}
		}
		dumper.close();
	}
	
	public static PrecisionResult run(XLog log, XLog alignedLog, DPNWithLayout dpn) throws Throwable {
		//	create new plugin	
		DataAwarePrecisionPlugin precisionRunner = new DataAwarePrecisionPlugin();
//		setup config
//		create an activity map that uses the exact mapping
		SetMultimap<String, Transition> activityMapping = HashMultimap.create();
		for(Transition trans: dpn.getDPN().getTransitions()) {
			activityMapping.put(trans.getLabel(), trans);
		}
//		create a variable mapping that uses the exact mapping
		System.out.println("[Job] Current dpn varaible size::"+dpn.getDPN().getVariables().size());
		Map<String,String> variableMapping = new HashMap<String,String>();
		variableMapping.put("d1","d1");
		System.out.println("[Job] variableMapping::");
		System.out.println(variableMapping.toString());
		System.out.println("[Job] updated dpn varaible size::"+dpn.getDPN().getVariables().size());
//		cast alignedLog to XAlignment
		XAlignedLog newAlignedLog = XAlignmentExtension.instance().extendLog(alignedLog);
		
		PrecisionConfig config = new PrecisionConfig(dpn.getDPN().getInitialMarking(), activityMapping,
				log.getClassifiers().get(0), variableMapping);
//		run measure
		PrecisionResult result = precisionRunner.doMeasurePrecisionWithAlignment(dpn.getDPN(), log, newAlignedLog, config);
		System.out.println(
				"[Job] Multi-perspective precision calulated: " +
				result.getPrecision()
		);
		return result;
		
	
	}
}
